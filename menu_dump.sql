--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

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
-- Name: menus; Type: TABLE; Schema: public; Owner: jake
--

CREATE TABLE public.menus (
    id integer NOT NULL,
    user_id integer NOT NULL,
    recipe_id integer
);


ALTER TABLE public.menus OWNER TO jake;

--
-- Name: menus_id_seq; Type: SEQUENCE; Schema: public; Owner: jake
--

CREATE SEQUENCE public.menus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_id_seq OWNER TO jake;

--
-- Name: menus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jake
--

ALTER SEQUENCE public.menus_id_seq OWNED BY public.menus.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: jake
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    displayname text NOT NULL,
    password text NOT NULL,
    menu_id integer
);


ALTER TABLE public.users OWNER TO jake;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: jake
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO jake;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jake
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: menus id; Type: DEFAULT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.menus ALTER COLUMN id SET DEFAULT nextval('public.menus_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: menus; Type: TABLE DATA; Schema: public; Owner: jake
--

COPY public.menus (id, user_id, recipe_id) FROM stdin;
16	1	\N
17	1	715544
19	1	754183
20	16	123
21	18	123
22	20	123
23	22	123
24	24	123
25	26	123
26	28	123
27	30	123
28	32	123
29	34	123
30	36	123
32	14	123
33	42	\N
34	44	\N
35	49	\N
36	54	\N
37	59	\N
39	60	\N
40	61	\N
41	62	\N
42	1	795514
43	65	\N
44	66	\N
45	67	\N
46	68	\N
47	1	123
48	1	123
49	1	123
50	69	\N
51	70	\N
52	71	\N
53	72	\N
54	73	\N
55	74	\N
56	71	637535
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jake
--

COPY public.users (id, username, displayname, password, menu_id) FROM stdin;
1	Lumb3rJake	LumberJakey	$2b$12$.U2yNcnpIjkPGpITX31UW.OmArDKNANtT0udrlYmC6p30cHUsoS1u	\N
14	testuser	Test User	testpassword	\N
15	testuser	Test User	testpassword	\N
16	testuser	Test User	testpassword	\N
17	testuser	Test User	testpassword	\N
18	testuser	Test User	testpassword	\N
19	testuser	Test User	testpassword	\N
20	testuser	Test User	testpassword	\N
21	testuser	Test User	testpassword	\N
22	testuser	Test User	testpassword	\N
23	testuser	Test User	testpassword	\N
24	testuser	Test User	testpassword	\N
25	testuser	Test User	testpassword	\N
26	testuser	Test User	testpassword	\N
27	testuser	Test User	testpassword	\N
28	testuser	Test User	testpassword	\N
29	testuser	Test User	testpassword	\N
30	testuser	Test User	testpassword	\N
31	testuser	Test User	testpassword	\N
32	testuser	Test User	testpassword	\N
33	testuser	Test User	testpassword	\N
34	testuser	Test User	testpassword	\N
35	testuser	Test User	testpassword	\N
36	testuser	Test User	testpassword	\N
37	testuser	Test User	testpassword	\N
38	testuser	Test User	testpassword	\N
39	testuser	Test User	testpassword	\N
40	testuser	Test User	testpassword	\N
41	testuser	Test User	$2b$12$kj05fECAx.u.9376Ts2gFeQMe.DD4qufgZosq7bPkXqEgwB3xmqTm	\N
42	newuser	New User	$2b$12$9qx.pFDTeGJc9CA7dKUEvuAc2QUDGNVh60rgORMJR1p6fgpry8BBy	\N
43	testuser	Test User	$2b$12$o0wHCWmB8mWFE4w7f87Oee7U.u6hoA/u/pxU3LoD7/qHmyzHiZX7G	\N
44	newuser	New User	$2b$12$sMI5jjkLwdb7AEqUy/U0/eNDVYTDS3jxYKn5nEDnUTSfin7SAKUXu	\N
45	testuser	Test User	$2b$12$EqL0Zz.0rqhX4SzNAqcqD.izcBCyT51rkeOT8y8ZRh3twav.pw0uu	\N
46	testuser	Test User	$2b$12$IltFyNJheKgidOo2k8xkEud/xRkOFRfkNrQBZN6rkjRTClUTk8gm.	\N
47	testuser	Test User	$2b$12$CEE5fgeS0pPr5VGpWE.hO.VCJrZf/vsnBBCoPLNrEIW9phyEwxkim	\N
48	testuser	Test User	$2b$12$6bfIc1.xxff/oHCBvwIJYudcgl89X8jb4p104nE5SmdzN5GU5Bagu	\N
49	newuser	New User	$2b$12$RdsVX2Pqd.41douf7PEBAu0np9G7pMv3f7MudY3C07ZgnBPbHwL7y	\N
50	testuser	Test User	$2b$12$ZRuCOVeBmdLYpsBgtS1zEONyJVYyG6rXcIY8wVvulnmPR9EIQYj5K	\N
51	testuser	Test User	$2b$12$UQPUPOKgmEnklNFc5SBsgO.WXwqDE1D/qkzaXnJVKgUVKpvrSwjv.	\N
52	testuser	Test User	$2b$12$/nsfAacTPYKFqZ0kGkyv2ejC5J.dZPfrVEhpApvamlDe8noLp7Cb2	\N
53	testuser	Test User	$2b$12$lcqPvWM/vvmLQ1eQUK7RU.z0Aj/ecrxkyOS4/5BnI60H2qJRqcARy	\N
54	newuser	New User	$2b$12$D1kvmL8J.g7j8h9WNRkvt.qz/oTsR4/75PbZMufZeBCa5pr5YC3UW	\N
55	testuser	Test User	$2b$12$rm/xni86lbuBnbshHmTSNeqU3Ri1zFJEJcZojLnJfls40JwimRcLy	\N
56	testuser	Test User	$2b$12$qlVhgnxA9lvvbo2itMaDHOxD/ss.TwEiONM1nc6b6kHYujUbrBAM.	\N
57	testuser	Test User	$2b$12$/M.cv9evpXdUTk2PTa3jE.vD2gK46Hc2uy1X/BQpTl7DDlgrrTDqa	\N
58	testuser	Test User	$2b$12$BX9Sy0W6GXT5sHEtDL61Pem1llpiqJ.2hEXkHctZMwwW65EG3DKw6	\N
59	newuser	New User	$2b$12$T9tv07GEYDpoSHo8ETbBJuAS44NeFFwbvxIMFQOteQtefI5HSk.rS	\N
60	Firehazord	fireyboi	$2b$12$AEAzG9Fkev0diGT2QZ/IuOgZvu11SIunM5Be/gqlifC7CxX4RNKP2	\N
61	testuser	Test User	$2b$12$9lLEP6PhCGhJeZUW22Q6AuAYkhsdAQHD7nJszpEgqkM3uTvrXYrba	\N
62	testuser	Test User	$2b$12$hMTmryK4IJJx0l3GcD2xeuzIk/yPfpvjk75MtcYuC13RmudA2HkzS	\N
63	testuser	Test User	$2b$12$DgFGvAyt4x88p6O4/4RGoujIXQcL0LovU398zMgt/HCjwJfBj2.HG	\N
64	testuser	Test User	$2b$12$tao/JQGjmKkgmTLX2weHJuIOl5FHJhFNIFJm26MkqysFvEvGu33Ha	\N
65	Lumb3rJake	LumberJakey	$2b$12$5HSexmhOgHwBqFryOSskSOHXn0p9FY/YA52eQfqqaVaNCTGO13tVe	\N
66	Lumb3rJake	LumberJakey	$2b$12$VVu1515Aa2BMvbJQVBp/Suxif6WucZswOM8prkFfyWtx2S/Vptpk.	\N
67	Lumb3rJake	LumberJakey	$2b$12$ZOZOHDJR/p2vYC.d1Uu6pOwzRbTf8yG46o3IzMHzyy8w5A7Zl/UQq	\N
68	Lumb3rJake	fireyboi	$2b$12$CqW67da1peUQNHxeDHgOSOu8wvHQvKrkK8bkhsrprD6/zottEQhcK	\N
69	TEST	Testy test	$2b$12$24ciJpSfaTV2IDxOAzbV3ewxFCdmclwZZsMWew1lVENcVjDgAEIyO	\N
70	jake	Testy test	$2b$12$01SF4IFDGQpMN947CUQ8J.E23P4a/TVtS0VsNIwC/v11Uue6UmQOO	\N
72	jake243	HiThere	$2b$12$o7SuWybRlRmc6keH3IyUj.R1txGrJWEOugclDDs3ZU32hZDPuC/y6	\N
73	jake2fda	HiThere	$2b$12$bd/Gs90Lh3vdXeF5oRO8Cu9fq6qL6NTiAt.AjvrnIQsUP4npkYgPy	\N
74	jake2dasfadsfasd	dfdasfasdfasdfasdf	$2b$12$BP1AzWbmfWv4h0FX7jDQfuJ79TZJy5P936KnZBAe61Uz5giOk/36i	\N
71	jake2fdsaf	Testy test	$2b$12$EffkCc47d5EuDFLtcrm7rOGCPG/cb4CC.5qWF8s.XVEgvNr4QOLcu	\N
\.


--
-- Name: menus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jake
--

SELECT pg_catalog.setval('public.menus_id_seq', 56, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jake
--

SELECT pg_catalog.setval('public.users_id_seq', 74, true);


--
-- Name: menus menus_pkey; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: menus fk_menus_user_id; Type: FK CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT fk_menus_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users fk_users_menu_id; Type: FK CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_menu_id FOREIGN KEY (menu_id) REFERENCES public.menus(id);


--
-- PostgreSQL database dump complete
--

