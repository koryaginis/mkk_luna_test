--
-- PostgreSQL database dump
--

\restrict Kqb5Nt1pyPjIPi83QOko2Duf9GlQ6hwM8EFOvih6lOdK905f4QLcLpJ3IvkrzSH

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.activities (
    id integer NOT NULL,
    name character varying NOT NULL,
    path character varying NOT NULL
);


ALTER TABLE public.activities OWNER TO "user";

--
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.activities_id_seq OWNER TO "user";

--
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "user";

--
-- Name: buildings; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.buildings (
    id integer NOT NULL,
    country character varying,
    city character varying NOT NULL,
    street character varying NOT NULL,
    house_number character varying NOT NULL,
    latitude double precision,
    longitude double precision
);


ALTER TABLE public.buildings OWNER TO "user";

--
-- Name: buildings_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.buildings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.buildings_id_seq OWNER TO "user";

--
-- Name: buildings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.buildings_id_seq OWNED BY public.buildings.id;


--
-- Name: organizations; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.organizations (
    id integer NOT NULL,
    name character varying NOT NULL,
    building_id integer
);


ALTER TABLE public.organizations OWNER TO "user";

--
-- Name: organizations_activities; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.organizations_activities (
    organization_id integer NOT NULL,
    activity_id integer NOT NULL
);


ALTER TABLE public.organizations_activities OWNER TO "user";

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.organizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organizations_id_seq OWNER TO "user";

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.organizations_id_seq OWNED BY public.organizations.id;


--
-- Name: phones; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.phones (
    id integer NOT NULL,
    number character varying NOT NULL,
    organization_id integer
);


ALTER TABLE public.phones OWNER TO "user";

--
-- Name: phones_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.phones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phones_id_seq OWNER TO "user";

--
-- Name: phones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.phones_id_seq OWNED BY public.phones.id;


--
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- Name: buildings id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.buildings ALTER COLUMN id SET DEFAULT nextval('public.buildings_id_seq'::regclass);


--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.organizations ALTER COLUMN id SET DEFAULT nextval('public.organizations_id_seq'::regclass);


--
-- Name: phones id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.phones ALTER COLUMN id SET DEFAULT nextval('public.phones_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.activities (id, name, path) FROM stdin;
1	Автоуслуги	avtouslugi
5	Автоэлектрика	avtouslugi.avtoelektrika
6	Шиномонтаж	avtouslugi.shinomontazh
7	Кузовной ремонт	avtouslugi.kuzovnoi_remont
8	Балансировка колес	avtouslugi.shinomontazh.balansirovka_koles
9	Замена шин	avtouslugi.shinomontazh.zamena_shin
10	Установка сигнализаций	avtouslugi.avtoelektrika.ustanovka_signalizatsii
11	Установка магнитол	avtouslugi.avtoelektrika.ustanovka_magnitol
12	Покраска деталей	avtouslugi.kuzovnoi_remont.pokraska_detalei
13	Ремонт вмятин	avtouslugi.kuzovnoi_remont.remont_vmiatin
14	Красота и здоровье	krasota_i_zdorove
15	Татуировка	krasota_i_zdorove.tatuirovka
16	Маникюр	krasota_i_zdorove.manikiur
17	Парикмахерские услуги	krasota_i_zdorove.parikmakherskie_uslugi
18	Разработка эскиза	krasota_i_zdorove.tatuirovka.razrabotka_eskiza
19	Нанесение тату	krasota_i_zdorove.tatuirovka.nanesenie_tatu
20	Классический маникюр	krasota_i_zdorove.manikiur.klassicheskii_manikiur
21	Аппаратный маникюр	krasota_i_zdorove.manikiur.apparatnyi_manikiur
22	Стрижка	krasota_i_zdorove.parikmakherskie_uslugi.strizhka
23	Окрашивание волос	krasota_i_zdorove.parikmakherskie_uslugi.okrashivanie_volos
24	Ремонт и строительство	remont_i_stroitelstvo
25	Сантехника	remont_i_stroitelstvo.santekhnika
26	Электрика	remont_i_stroitelstvo.elektrika
27	Отделка	remont_i_stroitelstvo.otdelka
28	Установка смесителей	remont_i_stroitelstvo.santekhnika.ustanovka_smesitelei
29	Замена труб	remont_i_stroitelstvo.santekhnika.zamena_trub
30	Монтаж проводки	remont_i_stroitelstvo.elektrika.montazh_provodki
31	Установка розеток и выключателей	remont_i_stroitelstvo.elektrika.ustanovka_rozetok_i_vykliuchatelei
32	Малярные работы	remont_i_stroitelstvo.otdelka.maliarnye_raboty
33	Укладка плитки	remont_i_stroitelstvo.otdelka.ukladka_plitki
34	Образование	obrazovanie
35	Языковые курсы	obrazovanie.iazykovye_kursy
36	Творческие курсы	obrazovanie.tvorcheskie_kursy
37	Технические курсы	obrazovanie.tekhnicheskie_kursy
38	Английский язык	obrazovanie.iazykovye_kursy.angliiskii_iazyk
39	Испанский язык	obrazovanie.iazykovye_kursy.ispanskii_iazyk
40	Рисование	obrazovanie.tvorcheskie_kursy.risovanie
41	Фотография	obrazovanie.tvorcheskie_kursy.fotografiia
42	Программирование	obrazovanie.tekhnicheskie_kursy.programmirovanie
43	Робототехника	obrazovanie.tekhnicheskie_kursy.robototekhnika
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.alembic_version (version_num) FROM stdin;
5ef7a507fc68
\.


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.buildings (id, country, city, street, house_number, latitude, longitude) FROM stdin;
1	Россия	Томск	пр. Ленина	46	56.476482	84.949692
2	Россия	Томск	пр. Ленина	48	56.476885	84.949713
3	Россия	Томск	ул. Советская	48	56.477048	84.952602
4	Россия	Томск	пр. Фрунзе	7	56.476031	84.952559
5	Россия	Томск	ул. Степана Разина	19	56.482912	84.985331
6	Россия	Томск	ул. Сибирская	70	56.482845	84.989771
7	Россия	Томск	ул. Некрасова	6	56.483684	84.988219
8	Россия	Томск	ул. Дальне-Ключевская	16Б	56.50512	84.955533
9	Россия	Томск	ул. Большая Подгорная	93	56.504848	84.953393
10	Россия	Томск	ул. Большая Подгорная	87	56.503366	84.954243
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.organizations (id, name, building_id) FROM stdin;
1	Starline	5
2	Pandora	3
3	Шиномастер	2
4	WheelsPro	2
5	Шиномонтаж на Некрасова	7
6	Кузов70	10
7	AUTOMIXED	8
8	АвтоДом	7
9	Lunar Shapes	4
10	Module Tattoo	2
11	STK	3
12	ЦирюльникЪ	4
13	Mango	8
14	Barbie Studio	10
15	Водяной	10
16	Катод	10
17	Академия Ремонта	9
18	Малярия	3
19	Спец Мастер	5
20	Эврика	1
21	Территория Образования	6
22	Школа Гениев	7
23	Сказкина Школа	9
\.


--
-- Data for Name: organizations_activities; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.organizations_activities (organization_id, activity_id) FROM stdin;
1	10
1	11
2	10
2	11
3	8
3	9
4	9
4	8
5	8
5	9
6	12
6	13
7	13
7	12
8	12
8	13
8	8
8	9
8	10
8	11
7	9
7	10
9	18
9	19
10	19
10	18
11	18
11	19
9	22
9	23
11	20
11	21
12	22
12	23
13	20
13	21
14	18
14	19
14	20
14	21
14	22
14	23
15	28
15	29
16	30
16	31
17	31
17	30
17	32
17	33
17	28
17	29
18	32
19	28
19	29
19	30
19	31
20	42
20	43
20	38
20	39
21	38
21	39
21	40
21	41
21	42
21	43
22	43
22	42
22	38
22	39
23	40
23	41
\.


--
-- Data for Name: phones; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.phones (id, number, organization_id) FROM stdin;
1	tel:+7-921-456-78-23	1
2	tel:+7-999-120-45-67	2
3	tel:+7-927-334-65-42	3
4	tel:+7-938-204-11-58	4
5	tel:+7-916-782-49-30	5
6	tel:+7-985-213-77-64	6
7	tel:+7-964-508-92-13	7
8	tel:+7-977-665-14-78	8
9	tel:+7-901-389-07-55	9
10	tel:+7-915-478-29-36	10
11	tel:+7-962-821-44-17	11
12	tel:+7-902-157-63-80	12
13	tel:+7-909-334-22-91	13
14	tel:+7-996-475-90-68	14
15	tel:+7-928-730-55-24	15
16	tel:+7-987-241-18-72	16
17	tel:+7-953-600-47-31	17
18	tel:+7-906-882-39-14	18
19	tel:+7-961-530-78-25	19
20	tel:+7-900-114-92-86	20
21	tel:+7-981-775-08-49	21
22	tel:+7-904-368-51-97	22
23	tel:+7-999-000-12-34	23
\.


--
-- Name: activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.activities_id_seq', 43, true);


--
-- Name: buildings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.buildings_id_seq', 10, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.organizations_id_seq', 23, true);


--
-- Name: phones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.phones_id_seq', 23, true);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);


--
-- Name: organizations_activities organizations_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.organizations_activities
    ADD CONSTRAINT organizations_activities_pkey PRIMARY KEY (organization_id, activity_id);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: phones phones_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY (id);


--
-- Name: ix_activities_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_activities_id ON public.activities USING btree (id);


--
-- Name: ix_buildings_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_buildings_id ON public.buildings USING btree (id);


--
-- Name: ix_organizations_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_organizations_id ON public.organizations USING btree (id);


--
-- Name: ix_phones_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_phones_id ON public.phones USING btree (id);


--
-- Name: organizations_activities organizations_activities_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.organizations_activities
    ADD CONSTRAINT organizations_activities_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id);


--
-- Name: organizations_activities organizations_activities_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.organizations_activities
    ADD CONSTRAINT organizations_activities_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: organizations organizations_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.buildings(id);


--
-- Name: phones phones_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- PostgreSQL database dump complete
--

\unrestrict Kqb5Nt1pyPjIPi83QOko2Duf9GlQ6hwM8EFOvih6lOdK905f4QLcLpJ3IvkrzSH

