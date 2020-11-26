
CREATE OR REPLACE FUNCTION public.anonymize_db(hash_f character varying(20))
  RETURNS void AS
$BODY$
DECLARE random_num numeric;
DECLARE random_char character varying;
DECLARE random_hash_char character varying(100);
DECLARE enc_ide character varying;--
DECLARE enc_num character varying;
DECLARE pat_ide character varying;--
DECLARE pat_num character varying;
DECLARE substring character varying;

BEGIN
raise notice '**** This is the latest (until the next one...) version of the random hashing running...!!! ****';
CREATE EXTENSION IF NOT EXISTS pgcrypto;--load pgcrypto so as to have all cryptographic functions available
ALTER TABLE encounter_mapping ALTER COLUMN encounter_num TYPE character varying(100);
ALTER TABLE observation_fact ALTER COLUMN encounter_num TYPE character varying(100);
ALTER TABLE observation_fact ALTER COLUMN patient_num TYPE character varying(100);
ALTER TABLE patient_dimension ALTER COLUMN patient_num TYPE character varying(100);
ALTER TABLE patient_mapping ALTER COLUMN patient_num TYPE character varying(100);
ALTER TABLE visit_dimension ALTER COLUMN encounter_num TYPE character varying(100);
ALTER TABLE visit_dimension ALTER COLUMN patient_num TYPE character varying(100);

for enc_ide in 
	SELECT encounter_ide
	FROM encounter_mapping
loop
	BEGIN
		random_num := enc_ide::integer + (SELECT random()*100);
		random_hash_char := (SELECT encode(digest(random_num::character varying, hash_f), 'hex'));--<------<--------
	EXCEPTION
		--random_char := enc_ide::character varying || (SELECT random()*100):character varying;
		WHEN others THEN
		 random_char := enc_ide::character varying || (SELECT random()*100);
		 random_hash_char := (SELECT encode(digest(random_char::character varying, hash_f), 'hex'));--<------<--------
	END;
		--raise notice 'Encounter_ide: %  --> random_num: %  --> random_hash: %', enc_ide, random_num, random_hash_char;
		UPDATE encounter_mapping SET encounter_ide=random_hash_char WHERE encounter_ide=enc_ide;
end loop;
raise notice '** Done with randomly hashing the encounter_ide s **';
for enc_num in
	SELECT encounter_num
	FROM encounter_mapping
loop
	random_num := enc_num::integer + (SELECT random()*100);
	random_hash_char := (SELECT encode(digest(random_num::character varying, hash_f), 'hex'));--<------<--------
	--raise notice 'Encounter_num: %  --> random_num: %  --> random_hash: %', enc_num, random_num, random_hash_char;	
	UPDATE encounter_mapping SET encounter_num=random_hash_char WHERE encounter_num=enc_num;
	UPDATE observation_fact SET encounter_num=random_hash_char WHERE encounter_num=enc_num;
	UPDATE visit_dimension SET encounter_num=random_hash_char WHERE encounter_num=enc_num;
end loop;
raise notice '** Done with randomly hashing the encounter_num s **';
for pat_ide in 
	SELECT patient_ide
	FROM patient_mapping
loop
	BEGIN
		random_num := pat_ide::integer + (SELECT random()*100);
		random_hash_char := (SELECT encode(digest(random_num::character varying, hash_f), 'hex'));--<------<--------
	EXCEPTION
		WHEN others THEN
		random_char := pat_ide::character varying || (SELECT random()*100);
		random_hash_char := (SELECT encode(digest(random_char::character varying, hash_f), 'hex'));--<------<--------
	END;
		--raise notice 'PAtient_ide: FR_%  --> random_num: %  --> random_hash: %', pat_ide, random_num, random_hash_char;
		UPDATE patient_mapping SET patient_ide=random_hash_char WHERE patient_ide=pat_ide;
		UPDATE encounter_mapping SET patient_ide=random_hash_char WHERE patient_ide=pat_ide;
end loop;
raise notice '** Done with randomly hashing the patient_ide s **';
for pat_num in
	SELECT patient_num
	FROM patient_mapping
loop
	random_num := pat_num::integer + (SELECT random()*100);
	random_hash_char := (SELECT encode(digest(random_num::character varying, hash_f), 'hex'));--<------<--------
	--raise notice 'PAtient_num: %  --> random_num: %  --> random_hash: %', pat_num, random_num, random_hash_char;	
	UPDATE observation_fact SET patient_num=random_hash_char WHERE patient_num=pat_num;
	UPDATE patient_dimension SET patient_num=random_hash_char WHERE patient_num=pat_num;
	UPDATE patient_mapping SET patient_num=random_hash_char WHERE patient_num=pat_num;
	UPDATE visit_dimension SET patient_num=random_hash_char WHERE patient_num=pat_num;
end loop;
raise notice '** Done with randomly hashing the patient_num s **';


END; $BODY$
  LANGUAGE plpgsql;
--select anonymize_db('sha224'); run select from bash or python with the cypto_function that we prefer
