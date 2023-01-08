-- creating the STUDENT users --

 set serveroutput on
 DECLARE
   cre_students VARCHAR2 (200);
   grant_students VARCHAR2 (200);
   default_tablespace VARCHAR2 (200);
   Number_of_students number (10);
BEGIN
   Default_tablespace:='&default_tablespace';
   Number_of_students:='&Number_of_students';
  for i in 1..Number_of_students LOOP
   cre_students :=
         'CREATE USER student'||i
	  ||' IDENTIFIED BY oracle '
      || ' DEFAULT TABLESPACE '||default_tablespace
      || ' QUOTA UNLIMITED ON '||default_tablespace;
    grant_students :=
	'GRANT CREATE SESSION,RESOURCE,CREATE VIEW TO student'||i;
   EXECUTE IMMEDIATE (cre_students);
   EXECUTE IMMEDIATE (grant_students);
end loop;
end;
/

