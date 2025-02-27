SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE FUNCTION public.cost_calculate() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_type_id int;
    v_price numeric(10,2);
    v_session_time int;
BEGIN
    v_session_time := floor(random() * 11)::int;
    SELECT type_id INTO v_type_id
    FROM vehicles
    WHERE plate_number = NEW.plate_number;
    SELECT price INTO v_price
    FROM vehicle_type
    WHERE type_id = v_type_id;
    NEW.session_time := v_session_time;
    NEW.cost := v_price * v_session_time;
    RETURN NEW;
END;
$$;

ALTER FUNCTION public.cost_calculate() OWNER TO postgres;

CREATE PROCEDURE public.end_day_ops()
    LANGUAGE plpgsql
    AS $$
DECLARE
    last_id BIGINT;
BEGIN
    TRUNCATE vehicles;
    SELECT COALESCE(MAX(record_id), 0) INTO last_id FROM parking_records;
    PERFORM setval('parking_records_record_id_seq', last_id + 1, false);
    UPDATE system_info SET last_end_day_id = last_id WHERE id = 1;
END;
$$;

ALTER PROCEDURE public.end_day_ops() OWNER TO postgres;

CREATE FUNCTION public.reuse_user_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    new_id INT;
BEGIN
    SELECT MIN(a.user_id + 1) INTO new_id
    FROM users a
    WHERE NOT EXISTS (
        SELECT 1
        FROM users b
        WHERE b.user_id = a.user_id + 1
    );
    IF new_id IS NOT NULL AND new_id < OLD.user_id THEN
        UPDATE users
        SET user_id = new_id
        WHERE user_id = OLD.user_id;
    END IF;
    RETURN NEW;
END;
$$;

ALTER FUNCTION public.reuse_user_id() OWNER TO postgres;

SET default_tablespace = '';
SET default_table_access_method = heap;

CREATE TABLE public.parking_records (
    record_id integer NOT NULL,
    plate_number character varying(20),
    entry_time timestamp without time zone NOT NULL,
    cost numeric(10,2),
    session_time integer,
    user_id integer
);

ALTER TABLE public.parking_records OWNER TO postgres;

CREATE SEQUENCE public.parking_records_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.parking_records_record_id_seq OWNER TO postgres;
ALTER SEQUENCE public.parking_records_record_id_seq OWNED BY public.parking_records.record_id;

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    role_description text
);

ALTER TABLE public.roles OWNER TO postgres;

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.roles_role_id_seq OWNER TO postgres;
ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;

CREATE TABLE public.system_info (
    id integer NOT NULL,
    last_end_day_id bigint DEFAULT 0
);

ALTER TABLE public.system_info OWNER TO postgres;

CREATE SEQUENCE public.system_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.system_info_id_seq OWNER TO postgres;
ALTER SEQUENCE public.system_info_id_seq OWNED BY public.system_info.id;

CREATE VIEW public.total_earnings_view AS
 SELECT sum(parking_records.cost) AS total_earnings
   FROM public.parking_records
  WHERE (parking_records.record_id > ( SELECT system_info.last_end_day_id
           FROM public.system_info
          WHERE (system_info.id = 1)));

ALTER TABLE public.total_earnings_view OWNER TO postgres;

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying(50) NOT NULL,
    password character varying(100),
    role_id integer
);

ALTER TABLE public.users OWNER TO postgres;

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.users_user_id_seq OWNER TO postgres;
ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;

CREATE TABLE public.vehicle_type (
    type_id integer NOT NULL,
    type_name character varying(50) NOT NULL,
    price numeric(10,2)
);

ALTER TABLE public.vehicle_type OWNER TO postgres;

CREATE TABLE public.vehicles (
    plate_number character varying(20) NOT NULL,
    type_id integer,
    is_detected boolean NOT NULL
);

ALTER TABLE public.vehicles OWNER TO postgres;

CREATE VIEW public.vehicle_income_view AS
 SELECT vt.type_name AS "Vehicle Type",
    count(pr.plate_number) AS "Vehicle Count",
    sum(pr.cost) AS "Total Income"
   FROM ((public.parking_records pr
     JOIN public.vehicles v ON (((pr.plate_number)::text = (v.plate_number)::text)))
     JOIN public.vehicle_type vt ON ((v.type_id = vt.type_id)))
  WHERE (pr.cost IS NOT NULL)
  GROUP BY vt.type_name;

ALTER TABLE public.vehicle_income_view OWNER TO postgres;
    count(pr.plate_number) AS "Araç Sayısı",
    sum(pr.cost) AS "Toplam Kazanç"
   FROM ((public.parking_records pr
     JOIN public.vehicles v ON (((pr.plate_number)::text = (v.plate_number)::text)))
     JOIN public.vehicle_type vt ON ((v.type_id = vt.type_id)))
  WHERE (pr.cost IS NOT NULL)
  GROUP BY vt.type_name;

ALTER TABLE public.vehicle_income_view OWNER TO postgres;

CREATE SEQUENCE public.vehicle_type_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.vehicle_type_type_id_seq OWNER TO postgres;
ALTER SEQUENCE public.vehicle_type_type_id_seq OWNED BY public.vehicle_type.type_id;
ALTER TABLE ONLY public.parking_records ALTER COLUMN record_id SET DEFAULT nextval('public.parking_records_record_id_seq'::regclass);
ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);
ALTER TABLE ONLY public.system_info ALTER COLUMN id SET DEFAULT nextval('public.system_info_id_seq'::regclass);
ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
ALTER TABLE ONLY public.vehicle_type ALTER COLUMN type_id SET DEFAULT nextval('public.vehicle_type_type_id_seq'::regclass);

ALTER TABLE ONLY public.parking_records ADD CONSTRAINT parking_records_pkey PRIMARY KEY (record_id);
ALTER TABLE ONLY public.roles ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);
ALTER TABLE ONLY public.system_info ADD CONSTRAINT system_info_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users ADD CONSTRAINT unique_user_name UNIQUE (user_name);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
ALTER TABLE ONLY public.vehicle_type ADD CONSTRAINT vehicle_type_pkey PRIMARY KEY (type_id);
ALTER TABLE ONLY public.vehicles ADD CONSTRAINT vehicles_pkey PRIMARY KEY (plate_number);

CREATE TRIGGER parking_records_cost_trigger BEFORE INSERT ON public.parking_records FOR EACH ROW EXECUTE FUNCTION public.cost_calculate();
CREATE TRIGGER reuse_id_trigger AFTER DELETE ON public.users FOR EACH ROW EXECUTE FUNCTION public.reuse_user_id();

ALTER TABLE ONLY public.parking_records ADD CONSTRAINT fk_parking_records_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);
ALTER TABLE ONLY public.vehicles ADD CONSTRAINT vehicles_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.vehicle_type(type_id);

