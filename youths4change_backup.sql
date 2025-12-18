l--
-- PostgreSQL database dump
--

\restrict Js8w4cWXBPzLy9rhQFiC0Tf2RVk2QE8IW6hovmWTWgEYnWUkTJ2OJrIscaAwIRL

-- Dumped from database version 17.7 (178558d)
-- Dumped by pg_dump version 17.7 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: admins; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(100),
    role character varying(50) DEFAULT 'admin'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.admins OWNER TO neondb_owner;

--
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO neondb_owner;

--
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- Name: applications; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.applications (
    id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(20) NOT NULL,
    country character varying(100) NOT NULL,
    motivation text NOT NULL,
    status character varying(50) DEFAULT 'pending'::character varying,
    applied_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    reviewed_at timestamp without time zone
);


ALTER TABLE public.applications OWNER TO neondb_owner;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.applications_id_seq OWNER TO neondb_owner;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.applications_id_seq OWNED BY public.applications.id;


--
-- Name: contact_info; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.contact_info (
    id integer NOT NULL,
    contact_type character varying(50) NOT NULL,
    label character varying(100),
    value text NOT NULL,
    link text,
    icon character varying(50),
    order_position integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.contact_info OWNER TO neondb_owner;

--
-- Name: contact_info_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.contact_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contact_info_id_seq OWNER TO neondb_owner;

--
-- Name: contact_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.contact_info_id_seq OWNED BY public.contact_info.id;


--
-- Name: core_values; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.core_values (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    icon character varying(50) NOT NULL,
    order_position integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.core_values OWNER TO neondb_owner;

--
-- Name: core_values_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.core_values_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.core_values_id_seq OWNER TO neondb_owner;

--
-- Name: core_values_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.core_values_id_seq OWNED BY public.core_values.id;


--
-- Name: countries; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.countries (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    flag_icon character varying(255),
    member_count integer DEFAULT 0,
    active_projects_count integer DEFAULT 0
);


ALTER TABLE public.countries OWNER TO neondb_owner;

--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.countries_id_seq OWNER TO neondb_owner;

--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.countries_id_seq OWNED BY public.countries.id;


--
-- Name: donations; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.donations (
    id integer NOT NULL,
    donor_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    amount numeric(10,2) NOT NULL,
    project_id integer,
    country character varying(100),
    status character varying(50) DEFAULT 'completed'::character varying,
    donation_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    transaction_id character varying(255),
    payment_method character varying(50),
    currency character varying(10) DEFAULT 'GHS'::character varying,
    payment_status character varying(20) DEFAULT 'pending'::character varying,
    flw_ref character varying(255)
);


ALTER TABLE public.donations OWNER TO neondb_owner;

--
-- Name: donations_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.donations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.donations_id_seq OWNER TO neondb_owner;

--
-- Name: donations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.donations_id_seq OWNED BY public.donations.id;


--
-- Name: founder; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.founder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    bio text NOT NULL,
    image_url text,
    image_public_id character varying(255),
    email character varying(255),
    linkedin_url text,
    twitter_url text,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.founder OWNER TO neondb_owner;

--
-- Name: founder_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.founder_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.founder_id_seq OWNER TO neondb_owner;

--
-- Name: founder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.founder_id_seq OWNED BY public.founder.id;


--
-- Name: members; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.members (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    role_in_org character varying(100),
    country character varying(100),
    email character varying(255),
    joined_date date DEFAULT CURRENT_DATE
);


ALTER TABLE public.members OWNER TO neondb_owner;

--
-- Name: members_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_id_seq OWNER TO neondb_owner;

--
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- Name: page_content; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.page_content (
    id integer NOT NULL,
    page_name character varying(100) NOT NULL,
    section_key character varying(100) NOT NULL,
    content_value text NOT NULL,
    content_type character varying(50) DEFAULT 'text'::character varying,
    order_position integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    cloudinary_public_id character varying(255)
);


ALTER TABLE public.page_content OWNER TO neondb_owner;

--
-- Name: page_content_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.page_content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.page_content_id_seq OWNER TO neondb_owner;

--
-- Name: page_content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.page_content_id_seq OWNED BY public.page_content.id;


--
-- Name: project_images; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.project_images (
    id integer NOT NULL,
    project_id integer NOT NULL,
    cloudinary_public_id character varying(255) NOT NULL,
    caption text,
    order_position integer DEFAULT 0,
    uploaded_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.project_images OWNER TO neondb_owner;

--
-- Name: project_images_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.project_images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_images_id_seq OWNER TO neondb_owner;

--
-- Name: project_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.project_images_id_seq OWNED BY public.project_images.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    country character varying(100),
    beneficiaries_count integer DEFAULT 0,
    budget numeric(10,2),
    status character varying(50) DEFAULT 'active'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    cloudinary_public_id character varying(255)
);


ALTER TABLE public.projects OWNER TO neondb_owner;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_id_seq OWNER TO neondb_owner;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: regional_offices; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.regional_offices (
    id integer NOT NULL,
    country character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(50) NOT NULL,
    address text,
    is_active boolean DEFAULT true,
    order_position integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.regional_offices OWNER TO neondb_owner;

--
-- Name: regional_offices_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.regional_offices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.regional_offices_id_seq OWNER TO neondb_owner;

--
-- Name: regional_offices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.regional_offices_id_seq OWNED BY public.regional_offices.id;


--
-- Name: site_settings; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.site_settings (
    id integer NOT NULL,
    setting_key character varying(100) NOT NULL,
    setting_value text NOT NULL,
    setting_type character varying(50) DEFAULT 'text'::character varying,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.site_settings OWNER TO neondb_owner;

--
-- Name: site_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.site_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.site_settings_id_seq OWNER TO neondb_owner;

--
-- Name: site_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.site_settings_id_seq OWNED BY public.site_settings.id;


--
-- Name: social_media; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.social_media (
    id integer NOT NULL,
    platform character varying(50) NOT NULL,
    platform_name character varying(100) NOT NULL,
    url text NOT NULL,
    icon character varying(50),
    color_class character varying(100),
    is_active boolean DEFAULT true,
    order_position integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.social_media OWNER TO neondb_owner;

--
-- Name: social_media_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.social_media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.social_media_id_seq OWNER TO neondb_owner;

--
-- Name: social_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.social_media_id_seq OWNED BY public.social_media.id;


--
-- Name: team_members; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.team_members (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "position" character varying(255) NOT NULL,
    role_type character varying(50) NOT NULL,
    bio text,
    image_url text,
    image_public_id character varying(255),
    email character varying(255),
    linkedin_url text,
    twitter_url text,
    country character varying(100),
    order_position integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.team_members OWNER TO neondb_owner;

--
-- Name: team_members_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.team_members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.team_members_id_seq OWNER TO neondb_owner;

--
-- Name: team_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.team_members_id_seq OWNED BY public.team_members.id;


--
-- Name: team_roles; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.team_roles (
    id integer NOT NULL,
    role_title character varying(100) NOT NULL,
    responsibilities text NOT NULL,
    order_position integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.team_roles OWNER TO neondb_owner;

--
-- Name: team_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.team_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.team_roles_id_seq OWNER TO neondb_owner;

--
-- Name: team_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.team_roles_id_seq OWNED BY public.team_roles.id;


--
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- Name: applications id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.applications ALTER COLUMN id SET DEFAULT nextval('public.applications_id_seq'::regclass);


--
-- Name: contact_info id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contact_info ALTER COLUMN id SET DEFAULT nextval('public.contact_info_id_seq'::regclass);


--
-- Name: core_values id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.core_values ALTER COLUMN id SET DEFAULT nextval('public.core_values_id_seq'::regclass);


--
-- Name: countries id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.countries ALTER COLUMN id SET DEFAULT nextval('public.countries_id_seq'::regclass);


--
-- Name: donations id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.donations ALTER COLUMN id SET DEFAULT nextval('public.donations_id_seq'::regclass);


--
-- Name: founder id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.founder ALTER COLUMN id SET DEFAULT nextval('public.founder_id_seq'::regclass);


--
-- Name: members id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- Name: page_content id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.page_content ALTER COLUMN id SET DEFAULT nextval('public.page_content_id_seq'::regclass);


--
-- Name: project_images id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_images ALTER COLUMN id SET DEFAULT nextval('public.project_images_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: regional_offices id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.regional_offices ALTER COLUMN id SET DEFAULT nextval('public.regional_offices_id_seq'::regclass);


--
-- Name: site_settings id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.site_settings ALTER COLUMN id SET DEFAULT nextval('public.site_settings_id_seq'::regclass);


--
-- Name: social_media id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.social_media ALTER COLUMN id SET DEFAULT nextval('public.social_media_id_seq'::regclass);


--
-- Name: team_members id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_members ALTER COLUMN id SET DEFAULT nextval('public.team_members_id_seq'::regclass);


--
-- Name: team_roles id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_roles ALTER COLUMN id SET DEFAULT nextval('public.team_roles_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.admins (id, username, email, password_hash, full_name, role, created_at, updated_at) FROM stdin;
3	admin	inares.tsangue@ashesi.edu.gh	$2b$12$rg9bpq/EKexOoUPTyzX/Z.nxiVZRyXeeMwlZB/MxHxDKdhjHkjgOm	Inares Kenne Tsangue	admin	2025-11-29 17:59:11.516045	2025-11-29 17:59:11.516045
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.applications (id, full_name, email, phone, country, motivation, status, applied_at, reviewed_at) FROM stdin;
4	Inares Kenne Tsangue	tsangueinares@gmail.com	+237653417287	Cameroon	Every day I wake up driven by a simple but powerful belief: positive change begins with ordinary people who choose to act. My journey has taught me that challenges are not barriers; they are opportunities to grow, lead, and uplift others. Coming from a background where I had to work hard to support my education, I developed resilience, discipline, and a deep commitment to service. These values shaped my passion for empowering young people and fostering communities where everyone has the chance to thrive.\n\nThrough my work with the Youths4Change initiative, I have seen firsthand how guidance, education, and compassion can transform lives. Whether it is teaching students about menstrual hygiene, helping them plant trees for a greener future, or supporting vulnerable communities, every action reinforces my commitment to building a better world.\n\nI am motivated by the impact that even small efforts can create. I believe in solutions that are practical, inclusive, and sustainable. I am not just working to change circumstances—I am working to inspire others to believe in what is possible.\n\nThis motivation fuels my dedication, sharpens my vision, and strengthens my resolve to keep learning, serving, and leading with purpose.	approved	2025-11-19 19:04:39.421074	2025-11-28 15:10:58.603809
3	Kwame Mensah	kwamemensah@gmail.com	+233244123456	Ghana	I am deeply passionate about youth empowerment and community development. Growing up in a rural community, I witnessed firsthand the challenges that young people face in accessing quality education and opportunities. This experience has shaped my commitment to creating positive change. I have been volunteering with local youth organizations for the past three years, where I have gained valuable experience in organizing educational workshops and mentorship programs. I believe that joining Youths4Change will allow me to expand my impact and learn from a network of like-minded young leaders across Africa. I am particularly interested in your educational initiatives and would love to contribute my skills in project coordination and community mobilization. I am committed to dedicating my time and energy to advancing the mission of Youths4Change and making a meaningful difference in the lives of young people across our continent.	rejected	2025-11-17 19:03:00.711012	2025-11-28 15:11:05.023061
2	Kwame Mensah	kwamemensah@gmail.com	+233244123456	Ghana	I am deeply passionate about youth empowerment and community development. Growing up in a rural community, I witnessed firsthand the challenges that young people face in accessing quality education and opportunities. This experience has shaped my commitment to creating positive change. I have been volunteering with local youth organizations for the past three years, where I have gained valuable experience in organizing educational workshops and mentorship programs. I believe that joining Youths4Change will allow me to expand my impact and learn from a network of like-minded young leaders across Africa. I am particularly interested in your educational initiatives and would love to contribute my skills in project coordination and community mobilization. I am committed to dedicating my time and energy to advancing the mission of Youths4Change and making a meaningful difference in the lives of young people across our continent.	approved	2025-11-17 19:02:46.638409	2025-12-16 17:01:27.318672
1	Kwame Mensah	kwamemensah@gmail.com	+233244123456	Ghana	I am deeply passionate about youth empowerment and community development. Growing up in a rural community, I witnessed firsthand the challenges that young people face in accessing quality education and opportunities. This experience has shaped my commitment to creating positive change. I have been volunteering with local youth organizations for the past three years, where I have gained valuable experience in organizing educational workshops and mentorship programs. I believe that joining Youths4Change will allow me to expand my impact and learn from a network of like-minded young leaders across Africa. I am particularly interested in your educational initiatives and would love to contribute my skills in project coordination and community mobilization. I am committed to dedicating my time and energy to advancing the mission of Youths4Change and making a meaningful difference in the lives of young people across our continent.	approved	2025-11-17 19:00:57.42002	2025-12-16 17:01:36.041453
7	MAcalester 	m@gmail.com	+237653417287	Cameroon	I am excited to apply for this opportunity as it strongly aligns with my academic interests, leadership aspirations, and commitment to making a positive impact. I have consistently demonstrated responsibility, initiative, and resilience in both academic and community-based projects. I value collaboration, continuous learning, and integrity in all that I do. By participating in this program, I hope to deepen my skills, gain practical experience, and contribute actively to shared goals. I am confident that my enthusiasm, discipline, and strong work ethic will allow me to add value while growing professionally.and strong work ethic will allow me to add value while growing professionally.	approved	2025-12-16 17:00:14.874364	2025-12-16 17:01:01.98589
6	Tsangue Cyrille	ima@gmail.com	+237653393610	Cameroon	I am writing to express my strong interest in this opportunity. I am a highly motivated individual with a passion for learning, leadership, and impact-driven work. Through my academic journey and community engagements, I have developed strong problem-solving, teamwork, and communication skills. I thrive in environments that challenge me to think critically and contribute meaningfully. This opportunity aligns perfectly with my goals of personal growth and social impact, and I am eager to bring my dedication, adaptability, and commitment to excellence to your program while learning from experienced mentors and peers. Alsi, I play hand fall and I like going to 	approved	2025-12-16 16:59:16.286036	2025-12-16 17:01:05.369386
5	Tsangue Cyrille	j@gmail.com	+237653393610	Nigeria	I am writing to express my strong interest in joining Youths4Change (Y4C). I am deeply passionate about community development, youth empowerment, and creating sustainable social impact, which strongly aligns with the mission and values of Y4C.\n\nGrowing up, I witnessed firsthand the challenges faced by vulnerable individuals, especially young people who lack access to basic resources and opportunities. These experiences shaped my desire to contribute meaningfully to society and to be part of initiatives that drive positive change. Youths4Change stands out to me because of its commitment to empowering youth, promoting education, supporting menstrual health, and encouraging environmental sustainability.\n\nI am particularly inspired by Y4C’s initiatives such as EmpowerHer and GreenFuture, which address critical social and environmental issues in practical and impactful ways. I believe that sustainable change begins with education, awareness, and collective action, and I am eager to contribute my time, skills, and energy to support these programs.\n\nI bring with me a strong sense of responsibility, teamwork, and dedication to service. I am willing to learn, volunteer actively, and collaborate with others to help Y4C achieve its goals. Joining Youths4Change will not only allow me to serve my community but also help me grow as a leader and changemaker.\n\nThank you for considering my application. I would be honored to be part of Youths4Change and contribute to making a meaningful difference in the lives of others.\n	approved	2025-12-16 15:21:05.897683	2025-12-16 17:01:08.575595
\.


--
-- Data for Name: contact_info; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.contact_info (id, contact_type, label, value, link, icon, order_position, created_at, updated_at) FROM stdin;
3	address	Headquarters	Accra, Ghana	\N	MapPin	3	2025-11-22 10:22:57.127713	2025-11-29 16:45:59.415629
1	email	Email	tsangueinares@gmail.com	https://www.linkedin.com/company/youths4change-iniative/?viewAsMember=true	Mail	1	2025-11-22 10:22:57.127713	2025-12-11 10:26:33.158028
4	website	Website	www.youths4change.org	+237653417287	Globe	4	2025-11-22 10:22:57.127713	2025-12-12 09:20:06.704335
2	phone	Phone	+233 538154230	tel:+233538154230	Phone	2	2025-11-22 10:22:57.127713	2025-12-12 09:20:26.762301
\.


--
-- Data for Name: core_values; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.core_values (id, title, description, icon, order_position, is_active, created_at, updated_at) FROM stdin;
1	Empowerment	We believe in empowering young people to become leaders and change-makers in their communities.	Heart	1	t	2025-11-22 10:56:37.683754	2025-11-22 10:56:37.683754
2	Community	Building strong, supportive communities where young people can thrive and grow together.	Users	2	t	2025-11-22 10:56:37.683754	2025-11-22 10:56:37.683754
3	Impact	Creating measurable, sustainable impact through strategic projects and initiatives.	Target	3	t	2025-11-22 10:56:37.683754	2025-11-22 10:56:37.683754
4	Pan-African	Fostering unity and collaboration across eight African countries.	Globe	4	f	2025-11-22 10:56:37.683754	2025-11-22 10:56:37.683754
\.


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.countries (id, name, flag_icon, member_count, active_projects_count) FROM stdin;
1	Ghana	🇬🇭	5	2
2	Kenya	🇰🇪	3	1
3	Nigeria	🇳🇬	8	3
4	South Africa	🇿🇦	4	2
5	Uganda	🇺🇬	2	1
6	Tanzania	🇹🇿	3	1
7	Rwanda	🇷🇼	2	1
8	Cameroon	🇨🇲	4	2
\.


--
-- Data for Name: donations; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.donations (id, donor_name, email, amount, project_id, country, status, donation_date, transaction_id, payment_method, currency, payment_status, flw_ref) FROM stdin;
1	Kenne Tsangue Inares	tsangueinares@gmail.com	250.00	1	Cameroon	completed	2025-11-19 19:31:22.069171	\N	\N	GHS	pending	\N
2	Kenne Tsangue Inares	tsangueinares@gmail.com	250.00	1	Cameroon	completed	2025-11-19 19:31:26.771545	\N	\N	GHS	pending	\N
3	Kenne Tsangue Inares	tsangueinares@gmail.com	250.00	1	Cameroon	completed	2025-11-19 19:31:40.834309	\N	\N	GHS	pending	\N
4	Kenne Tsangue Inares	tsangueinares@gmail.com	100.00	1	Cameroon	completed	2025-11-19 19:33:34.166123	\N	\N	GHS	pending	\N
5	Tsangue Cyrille	joumenecyrille21@gmail.com	250.00	5	Ghana	completed	2025-11-29 14:26:33.589799	\N	\N	GHS	pending	\N
6	Tsangue Cyrille	joumenecyrille21@gmail.com	250.00	5	Ghana	completed	2025-11-29 14:26:40.824461	\N	\N	GHS	pending	\N
7	Bkwakiogbvgarbverqkab	xgurI@qjkbfa.com	1000.00	3	Uganda	completed	2025-12-11 11:34:52.677925	\N	\N	GHS	pending	\N
8	Bkwakiogbvgarbverqkab	xgurI@qjkbfa.com	1000.00	3	Uganda	completed	2025-12-11 11:34:58.863951	\N	\N	GHS	pending	\N
9	Ashesi University	qn@gmail.com	50.00	8	Cameroon	completed	2025-12-16 18:00:09.551862	\N	\N	GHS	pending	\N
10	Ashesi University	qn@gmail.com	50.00	8	Cameroon	completed	2025-12-16 18:00:14.685833	\N	\N	GHS	pending	\N
\.


--
-- Data for Name: founder; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.founder (id, name, title, bio, image_url, image_public_id, email, linkedin_url, twitter_url, is_active, created_at, updated_at) FROM stdin;
2	Founder Name	Founder & Executive Director	Inares Kenne Tsangue is the Founder and President of Youths4Change, a youth-driven initiative committed to empowering vulnerable communities through education, mentorship, and social impact projects. Growing up in a polygamous family and overcoming significant financial challenges, Inares learned early the importance of resilience, hard work, and compassion. To support his education, he often engaged in menial jobs—experiences that shaped his determination to create opportunities for others facing similar struggles.\n\nHis passion for community development and youth empowerment deepened as he advanced in school, ultimately inspiring him to establish the Youths4Change Initiative. Inares envisioned a platform where young people would not only receive support but also become agents of change in their communities. His drive is rooted in the belief that no young person should be held back by circumstances beyond their control.\n\nAs a Computer Science student at Ashesi University, Inares combines academic knowledge, leadership experience, and a deep sense of social responsibility to expand the reach and impact of Youths4Change. His leadership has birthed powerful projects such as EmpowerHer, which educates girls on menstrual hygiene and distributes sanitary pads, and GreenFuture, which engages students in environmental protection and tree-planting campaigns.\n\nThrough Youths4Change, Inares strives to build a generation of informed, confident, and socially responsible young leaders who are equipped and inspired to transform their communities. His vision is a world where young people—regardless of background—are empowered to rise, lead, and create sustainable change.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765534675/team/founder/ltvmpmmuhkvxxieozqwc.jpg	team/founder/ltvmpmmuhkvxxieozqwc	tsangueinares@gmail.com	www.linkedin.com/in/inares-kenne-tsangue	\N	t	2025-12-11 11:25:39.249116	2025-12-12 10:24:09.301144
1	Inares Kenne Tsangue	Founder & President	Inares Kenne Tsangue is the Founder and President of Youths4Change, a youth-driven initiative committed to empowering vulnerable communities through education, mentorship, and social impact projects. Growing up in a polygamous family and overcoming significant financial challenges, Inares learned early the importance of resilience, hard work, and compassion. To support his education, he often engaged in menial jobs—experiences that shaped his determination to create opportunities for others facing similar struggles.\n\nHis passion for community development and youth empowerment deepened as he advanced in school, ultimately inspiring him to establish the Youths4Change Initiative. Inares envisioned a platform where young people would not only receive support but also become agents of change in their communities. His drive is rooted in the belief that no young person should be held back by circumstances beyond their control.\n\nAs a Computer Science student at Ashesi University, Inares combines academic knowledge, leadership experience, and a deep sense of social responsibility to expand the reach and impact of Youths4Change. His leadership has birthed powerful projects such as EmpowerHer, which educates girls on menstrual hygiene and distributes sanitary pads, and GreenFuture, which engages students in environmental protection and tree-planting campaigns.\n\nThrough Youths4Change, Inares strives to build a generation of informed, confident, and socially responsible young leaders who are equipped and inspired to transform their communities. His vision is a world where young people—regardless of background—are empowered to rise, lead, and create sustainable change.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765534675/team/founder/ltvmpmmuhkvxxieozqwc.jpg	team/founder/ltvmpmmuhkvxxieozqwc	tsangueinares@gmail.com	www.linkedin.com/in/inares-kenne-tsangue	\N	t	2025-12-11 11:16:25.419757	2025-12-12 10:18:52.910534
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.members (id, name, role_in_org, country, email, joined_date) FROM stdin;
\.


--
-- Data for Name: page_content; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.page_content (id, page_name, section_key, content_value, content_type, order_position, created_at, updated_at, cloudinary_public_id) FROM stdin;
3	home	mission_preview	Youths4Change Initiative is a youth-led nonprofit organization dedicated to empowering young people across eight African countries to create positive change through education, mentorship, and sustainable development projects.	text	1	2025-11-22 10:56:37.51907	2025-11-22 10:56:37.51907	\N
2	about	hero_text	A youth-led nonprofit organization dedicated to empowering young people across Africa to create positive community change.	text	2	2025-11-22 10:56:37.51907	2025-12-16 13:16:18.156659	\N
1	about	our_story	Youths4Change Initiative was founded in 2023 by a group of passionate young leaders who recognized the immense potential of Africa's youth population. What started as a small grassroots movement in Ghana has grown into a pan-African organization operating across eight countries.\n\nOur founders witnessed firsthand the challenges young people face in accessing quality education, mentorship, and opportunities to develop their skills. They also saw the incredible talent, creativity, and determination that exists within African youth communities.\n\nSince our inception, we have:\n- Launched 12+ community development projects\n- Trained and mentored over 500 young leaders\n- Impacted more than 5,000 lives across eight countries\n- Created sustainable partnerships with local and international organizations\n- Built a network of youth ambassadors in every country we operate\n\nToday, Youths4Change continues to grow, driven by the passion and dedication of our team members, volunteers, and partners who believe in the power of youth-led change.	textarea	1	2025-11-22 10:56:37.51907	2025-12-16 13:16:21.695098	\N
\.


--
-- Data for Name: project_images; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.project_images (id, project_id, cloudinary_public_id, caption, order_position, uploaded_by, created_at, updated_at) FROM stdin;
14	10	youths4change/projects/bpstnvbvlcvvqzza8ocr		1	\N	2025-12-16 16:04:54.704608	2025-12-16 16:04:54.704608
16	10	youths4change/projects/io8gs1yqayy2aagmnosa		1	\N	2025-12-16 16:04:54.834131	2025-12-16 16:04:54.834131
15	10	youths4change/projects/ew0dwe8n6z59uy3an4a3		1	\N	2025-12-16 16:04:54.830452	2025-12-16 16:04:54.830452
17	10	youths4change/projects/astglxckiqhugbtsdfpn		1	\N	2025-12-16 16:04:54.83448	2025-12-16 16:04:54.83448
19	10	youths4change/projects/azo4hgcaa0673unmklzy		1	\N	2025-12-16 16:04:54.844316	2025-12-16 16:04:54.844316
18	10	youths4change/projects/ev7s1oki2cntmravbsyk		1	\N	2025-12-16 16:04:54.846222	2025-12-16 16:04:54.846222
20	10	youths4change/projects/ihfi2qwssqjpxhahwh8i		2	\N	2025-12-16 16:04:58.563952	2025-12-16 16:04:58.563952
21	10	youths4change/projects/lbjd72dfscdbfurtanto		2	\N	2025-12-16 16:04:58.840325	2025-12-16 16:04:58.840325
22	10	youths4change/projects/ctxqyujidgrqjw0okal9		2	\N	2025-12-16 16:04:58.843562	2025-12-16 16:04:58.843562
23	10	youths4change/projects/pbr6x0vsmycxmfiflnpn		2	\N	2025-12-16 16:04:58.848066	2025-12-16 16:04:58.848066
24	10	youths4change/projects/psjhvdqblu262xgin26g		2	\N	2025-12-16 16:04:58.932784	2025-12-16 16:04:58.932784
25	10	youths4change/projects/kpiwbfqg0lbw6cn66hsk		2	\N	2025-12-16 16:04:59.046499	2025-12-16 16:04:59.046499
26	10	youths4change/projects/hvlqlckb24vxivbtdkv7		3	\N	2025-12-16 16:05:02.047376	2025-12-16 16:05:02.047376
27	10	youths4change/projects/v2bhrfofvcy2kr215uu4		3	\N	2025-12-16 16:05:02.212997	2025-12-16 16:05:02.212997
28	10	youths4change/projects/mmyblzauchjf8bbxgnvn		3	\N	2025-12-16 16:05:02.221082	2025-12-16 16:05:02.221082
29	10	youths4change/projects/l67n2al1jxrgvnm4syo1		3	\N	2025-12-16 16:05:02.241289	2025-12-16 16:05:02.241289
30	10	youths4change/projects/w7c5gvgsqbcsxvw7ia3d		3	\N	2025-12-16 16:05:02.42983	2025-12-16 16:05:02.42983
31	10	youths4change/projects/fqccqi70epvwqlgyjx5h		3	\N	2025-12-16 16:05:03.537739	2025-12-16 16:05:03.537739
32	10	youths4change/projects/kgbg8sdfzxzcgab9z8ow		4	\N	2025-12-16 16:05:06.394731	2025-12-16 16:05:06.394731
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.projects (id, name, description, country, beneficiaries_count, budget, status, created_at, updated_at, cloudinary_public_id) FROM stdin;
3	Back to School	Supporting underprivileged children with school supplies and tuition	Sierra Leorne	200	25000.00	active	2025-11-16 17:36:51.530795	2025-12-16 13:10:13.591869	projects/u6yms7y9a5hzc2rnfmvq
2	GreenFuture	Environmental conservation and sustainability initiative for youth	Niger	85	10000.00	active	2025-11-16 17:36:51.530795	2025-12-16 13:12:13.397008	projects/upeh0nabfmakvq1e2zmp
1	EmpowerHer	A program focused on empowering young women through education and mentorship	Ghana	120	15000.00	active	2025-11-16 17:36:51.530795	2025-12-11 10:05:27.187241	youths4change/owyzsgtdbbjn8lrfxnzk
10	 Mentorship program	Our mentorship program is designed to support secondary school students through academic, personal, and career guidance. The program connects students with dedicated mentors who provide consistent support, motivation, and practical advice to help them navigate school life and make informed decisions about their future. Through interactive sessions, follow-ups, and one-on-one engagements, mentees build confidence, improve their academic performance, and develop essential life skills. The program emphasizes inclusivity, leadership development, and long-term impact, ensuring that students feel supported beyond each mentorship session.	Eswatini	167	500.00	completed	2025-12-16 13:32:19.675876	2025-12-16 13:32:19.675876	projects/i6jyg6thiedmbq5ypxqv
5	Visit to Elderly people	This initiative focuses on spending quality time with elderly members of the community to promote care, compassion, and social inclusion. Through visits to homes and care centers, volunteers engage the elderly in conversations, offer emotional support, and provide basic assistance and donated items where needed. The project aims to reduce loneliness, show appreciation for the elderly, and strengthen intergenerational bonds within the community.	Ghana	15	1000.00	active	2025-11-29 14:24:24.618723	2025-12-16 12:42:35.926834	projects/p0vxoi7bly9lcubvtwpo
4	Back to School Initiative	The Back to School initiative supports children from underserved communities by helping them return to school with confidence and the basic resources they need to learn. The project provides essential school supplies, learning materials, and motivational support to students at the start of the academic year. Through this initiative, we aim to reduce barriers to education, encourage school attendance, and inspire children to stay focused on their studies and future goals.	Cameroon	42	0.51	active	2025-11-24 17:47:40.397228	2025-12-16 12:44:23.485242	projects/aq3p6gje8dxfk4opsegy
8	GreenFuture	GreenFuture is an environmental initiative focused on empowering young people and school communities to take action on climate change and environmental sustainability. The program teaches primary and secondary school students how to plant trees, care for the environment, and start environmental clubs that continue advocacy and green practices beyond the initial engagement. Through hands-on activities, awareness campaigns, and community involvement, GreenFuture aims to build environmental stewardship from the ground up—instilling knowledge, responsibility, and long-term commitment to a greener future.	Cameroon	100	1000.00	active	2025-12-16 12:57:36.313759	2025-12-16 12:57:36.313759	projects/fiqwozso1st9cuymyid2
9	GreenFuture	GreenFuture is an environmental initiative focused on empowering young people and school communities to take action on climate change and environmental sustainability. The program teaches primary and secondary school students how to plant trees, care for the environment, and start environmental clubs that continue advocacy and green practices beyond the initial engagement. Through hands-on activities, awareness campaigns, and community involvement, GreenFuture aims to build environmental stewardship from the ground up—instilling knowledge, responsibility, and long-term commitment to a greener future.	Nigeria	100	1000.00	active	2025-12-16 13:00:51.514346	2025-12-16 13:01:27.471457	projects/vi1hvy6je8qj9kt4qivq
7	GreenFuture	GreenFuture is an environmental initiative focused on empowering young people and school communities to take action on climate change and environmental sustainability. The program teaches primary and secondary school students how to plant trees, care for the environment, and start environmental clubs that continue advocacy and green practices beyond the initial engagement. Through hands-on activities, awareness campaigns, and community involvement, GreenFuture aims to build environmental stewardship from the ground up—instilling knowledge, responsibility, and long-term commitment to a greener future.	South Sudan	100	1000.00	active	2025-12-16 12:57:12.849641	2025-12-16 13:09:23.235214	projects/qijaw6xry7otbkkymgoo
6	EmpowerHer	EmpowerHer is a community-focused initiative under Youths4Change aimed at promoting menstrual health education and dignity among young girls. The project educates students on menstrual hygiene, managing menstrual pain, and breaking common myths surrounding menstruation. It also engages boys and parents to foster understanding, reduce stigma, and create a supportive environment for girls both at school and at home. Through school outreach programs and the distribution of sanitary pads, EmpowerHer works to ensure that no girl misses school or feels ashamed because of her period.	DRC Congo	200	200.00	active	2025-12-10 22:13:40.917326	2025-12-16 16:39:22.995727	projects/x5uehumxazvp1hami3wx
\.


--
-- Data for Name: regional_offices; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.regional_offices (id, country, email, phone, address, is_active, order_position, created_at, updated_at) FROM stdin;
9	Ghana	tsangueinares@gmail.com	+237653417287	Accra	t	9	2025-11-29 17:03:56.230251	2025-11-29 17:03:56.230251
14	Niger	tsangueinares@gmail.com	+237653417287	Niamey	t	10	2025-12-12 09:11:40.473711	2025-12-12 09:11:40.473711
8	Cameroon	tsangueinares@gmail.com	+237653417287	Bamenda	t	8	2025-11-22 10:22:57.467279	2025-12-12 09:12:05.966066
15	Eswatini	tsangueinares@gmail.com	+237653417287	Bamenda	t	11	2025-12-12 09:13:39.476726	2025-12-12 09:13:39.476726
16	South Sudan	tsangueinares@gmail.com	+237653417287	Juba	t	12	2025-12-12 09:14:37.087537	2025-12-12 09:14:37.087537
17	Sierra Leorne	tsangueinares@gmail.com	+237653417287	Bamenda	t	13	2025-12-12 09:15:01.848476	2025-12-12 09:15:01.848476
18	DRC Congo	tsangueinares@gmail.com	+237653417287	Bamenda	t	14	2025-12-12 09:15:29.094145	2025-12-12 09:15:29.094145
19	Nigeria	tsangueinares@gmail.com	+237653417287	Abuja	t	15	2025-12-12 09:17:06.12304	2025-12-12 09:17:06.12304
\.


--
-- Data for Name: site_settings; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.site_settings (id, setting_key, setting_value, setting_type, description, created_at, updated_at) FROM stdin;
3	hero_description	Creating positive change across eight countries through education, mentorship, and sustainable development	text	Home page hero description	2025-11-22 10:56:37.354526	2025-12-16 17:16:28.226048
2	hero_heading	Empowering African Youth	text	Home page hero heading	2025-11-22 10:56:37.354526	2025-12-16 17:16:30.217786
8	hero_video_url	https://www.youtube.com/watch?v=gDhxKTZPDPo	text	YouTube or Vimeo video URL to display in the hero section (optional)	2025-12-16 16:48:31.082925	2025-12-16 17:16:31.936637
4	mission_statement	To empower young people across eight African countries to become agents of positive change through education, mentorship, and sustainable development projects. We provide platforms for youth leadership, skill development, and community engagement.	textarea	Organization mission statement	2025-11-22 10:56:37.354526	2025-12-16 17:16:33.665053
6	office_hours	Monday - Friday, 9:00 AM - 5:00 PM (GMT)	text	Office hours	2025-11-22 10:56:37.354526	2025-12-16 17:16:35.361341
7	response_time	We aim to respond to all inquiries within 24-48 hours	text	Expected response time	2025-11-22 10:56:37.354526	2025-12-16 17:16:37.067016
1	site_name	Youths4Change Initiative	text	Organization name	2025-11-22 10:56:37.354526	2025-12-16 17:16:38.887886
5	vision_statement	A future where every young person in Africa has the opportunity, resources, and support to reach their full potential and contribute meaningfully to their communities. We envision a continent led by empowered, innovative, and compassionate youth leaders.	textarea	Organization vision statement	2025-11-22 10:56:37.354526	2025-12-16 17:16:40.603475
\.


--
-- Data for Name: social_media; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.social_media (id, platform, platform_name, url, icon, color_class, is_active, order_position, created_at, updated_at) FROM stdin;
4	linkedin	LinkedIn	https://www.linkedin.com/company/youths4change-iniative/?viewAsMember=true	Linkedin	text-blue-700 hover:bg-blue-50	t	4	2025-11-22 10:22:57.293083	2025-12-11 10:27:19.842243
3	instagram	Instagram	https://www.instagram.com/youths4change_initiative/?hl=en	Instagram	text-pink-600 hover:bg-pink-50	t	3	2025-11-22 10:22:57.293083	2025-12-11 10:27:58.046576
1	facebook	Facebook	https://www.facebook.com/profile.php?id=61552340451425	Facebook	text-blue-600 hover:bg-blue-50	t	1	2025-11-22 10:22:57.293083	2025-12-11 10:35:48.166451
2	twitter	Twitter	https://twitter.com/youths4change	Twitter	text-sky-500 hover:bg-sky-50	f	2	2025-11-22 10:22:57.293083	2025-12-11 10:35:56.822303
5	tiktok	TikTok	https://www.tiktok.com/@youths4change_initiative?is_from_webapp=1&sender_device=pc	Globe	text-gray-800 hover:bg-gray-50	t	5	2025-12-11 10:37:03.69118	2025-12-11 10:37:03.69118
\.


--
-- Data for Name: team_members; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.team_members (id, name, "position", role_type, bio, image_url, image_public_id, email, linkedin_url, twitter_url, country, order_position, is_active, created_at, updated_at) FROM stdin;
5	Bryce Nembu	Volunteer Coordinator	executive		https://res.cloudinary.com/dsrca4ug2/image/upload/v1765535861/team/members/jo2ie6jzvxkumscunq2t.jpg	team/members/jo2ie6jzvxkumscunq2t	\N	\N	\N	Ghana	2	t	2025-12-11 11:25:40.038733	2025-12-12 10:38:33.114601
6	Fadzai Betty Mugobi	Executive	executive	Brief bio about this board member.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765536057/team/members/vvi0eweb0vgtbmv57ggn.jpg	team/members/vvi0eweb0vgtbmv57ggn	\N	\N	\N	Ghana	3	t	2025-12-11 11:25:40.038733	2025-12-12 10:41:06.789482
2	Kifayatu Hamza	Project Coordinator	executive	Kifayatu Hamza is a student at Ashesi University and a Mastercard Foundation Scholar, serving as the Project Coordinator at Youths4Change. She supports the planning and execution of youth-led initiatives focused on social impact, community engagement, and positive change. With a strong interest in leadership, culture, and development, she is passionate about empowering young people to turn ideas into meaningful action.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765535632/team/members/wwjxrhhyxwikwyl1c7et.jpg	team/members/wwjxrhhyxwikwyl1c7et	kifayatu.hamza@ashesi.edu.gh	http://www.linkedin.com/in/kifayatu-hamza	\N	Niger	2	t	2025-12-11 11:16:26.352784	2025-12-16 16:24:57.498038
33	Pascal 	Treasurer	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620707/team/members/jkccfk6yvtsdiklvappn.jpg	team/members/jkccfk6yvtsdiklvappn	\N	\N	\N	Ghana	0	t	2025-12-13 10:11:52.238979	2025-12-13 10:11:52.238979
36	Rayhan Abbas	Executive	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620812/team/members/pnjr77gdtnl57liigf0e.jpg	team/members/pnjr77gdtnl57liigf0e	\N	\N	\N	Eswatini	0	t	2025-12-13 10:13:40.542334	2025-12-16 16:24:35.872184
39	Median Yinyuy Ayuni	Financial Secretary	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765901731/youths4change/v707zvmp5ivdcmvtesu6.jpg	youths4change/v707zvmp5ivdcmvtesu6	\N	\N	\N	Cameroon	0	t	2025-12-16 16:15:56.791323	2025-12-16 16:15:56.791323
32	Tanaka	Project Coordinator	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620645/team/members/iayrvzslhpinpa2g32ym.jpg	team/members/iayrvzslhpinpa2g32ym	\N	\N	\N	Nigeria	0	t	2025-12-13 10:10:51.416237	2025-12-16 16:25:47.198169
37	Chiambah Tecla 	Regional coordinator for Bamenda	executive	My name is Chiambah Tecla Fienmoh, a motivated and detail-oriented graduate in Banking and Finance based in Cameroon. I am a Christian, guided by strong values of integrity, discipline, and service. I have experience in administrative support, typing, record management, and organizational tasks, with the ability to work accurately, independently, and responsibly. I am passionate about continuous learning, personal growth, and always happy when giving back to the community where I came from.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765901960/youths4change/rzrfj31cktnchrdtmvov.jpg	youths4change/rzrfj31cktnchrdtmvov	teclafien@gmail.com	https://www.facebook.com/share/17nyPJWf2c/	\N	Cameroon	0	t	2025-12-16 16:15:53.164751	2025-12-16 16:20:18.915377
35	Enoch	Executive	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620864/team/members/l7q0sqi22pda1rnerpod.jpg	team/members/l7q0sqi22pda1rnerpod	\N	\N	\N	DRC Congo	0	t	2025-12-13 10:13:39.217581	2025-12-16 16:24:08.545604
40	Yaounde	Executives	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765902073/youths4change/dhqael7uwr4g4cqduwrt.jpg	youths4change/dhqael7uwr4g4cqduwrt	\N	\N	\N	Cameroon	0	t	2025-12-16 16:21:40.214915	2025-12-16 16:22:00.957622
29	Acheampong Panin Darkwah	Executive	executive	My name is Acheampong Panin Darkwah, and I am a young individual with a strong interest in understanding how software and artificial intelligence have evolved and continue to shape our modern world. Beyond my passion for technology, I am deeply committed to community outreach, especially in supporting students, orphans, and teenage girls. Access to knowledge, mentorship, and the right tools can change lives, and I want to use technology as a means to empower young people and create learning opportunities for them to also grow up and make significant contributions to society.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620327/team/members/gjblntcxpr6qq2sdctaj.jpg	team/members/gjblntcxpr6qq2sdctaj	panindarkwah@gmail.com	www.linkedin.com/in/acheampong-darkwah	\N	DRC Congo	0	t	2025-12-13 10:06:24.042991	2025-12-16 16:23:56.71701
34	Charlotte Ayesu	General Secretary	executive	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620753/team/members/i0wigskfn8mo8pjxc8gl.jpg	team/members/i0wigskfn8mo8pjxc8gl	\N	\N	\N	Nigeria	0	t	2025-12-13 10:12:37.79225	2025-12-16 16:26:00.610143
28	Jeff	Assistant project coordinator	executive	asd	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620479/team/members/r44n8aqkgv6iv0ao1wo3.jpg	team/members/r44n8aqkgv6iv0ao1wo3	\N	\N	\N	Eswatini	0	t	2025-12-13 09:54:35.166173	2025-12-16 16:24:22.522057
30	Assistant Project Coordinator	Assistant project coordinator	executive	asd	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765620553/team/members/hgam9imzloya1wqsnvj9.jpg	team/members/hgam9imzloya1wqsnvj9	\N	\N	\N	Sierra Leorne	0	t	2025-12-13 10:08:39.242505	2025-12-16 16:26:25.728819
4	Miriam Miraji Samhina 	Public Relations Officer	executive	Miriam Miraji Samhina is a Business Administration student at Ashesi University, Ghana, and a purpose-driven emerging leader with over six years of leadership experience. She has served as President of the Rotaract Club of St. Jude and as a Course Representative at Ashesi, demonstrating a strong commitment to service and peer leadership. Miriam has gained practical experience through internships at Vision for Youth and The School of St. Jude, contributing to community relations, youth development initiatives, and organizational outreach. She is actively engaged in leadership networks including AYLF, HLD, and Y4C, and is passionate about values-based leadership and youth empowerment.	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765618570/team/members/m8bnxcf2odkzjinsioa1.jpg	team/members/m8bnxcf2odkzjinsioa1	mirimiraj03@gmail.com	https://www.linkedin.com/in/miriam-samhina-90b1a5299/	\N	Niger	1	t	2025-12-11 11:25:40.038733	2025-12-16 16:25:22.123558
42	Mevis Berry	Board Member	board	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765902768/youths4change/cgiglgcau5cwgacplmgy.jpg	youths4change/cgiglgcau5cwgacplmgy	\N	\N	\N	Cameroon	0	t	2025-12-16 16:33:44.353442	2025-12-16 16:33:44.353442
43	Eyram-Makafui Kofi Awoye 	Advisor	advisor	\N	https://res.cloudinary.com/dsrca4ug2/image/upload/v1765903057/youths4change/u1fpz3iidspvlqar6w4z.jpg	youths4change/u1fpz3iidspvlqar6w4z	\N	\N	\N	Ghana	0	t	2025-12-16 16:37:44.908701	2025-12-16 16:37:44.908701
\.


--
-- Data for Name: team_roles; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.team_roles (id, role_title, responsibilities, order_position, is_active, created_at, updated_at) FROM stdin;
1	Executive Director	Overall strategy and leadership	1	t	2025-11-22 10:56:37.846115	2025-11-22 10:56:37.846115
2	Program Coordinator	Project management and implementation	2	t	2025-11-22 10:56:37.846115	2025-11-22 10:56:37.846115
3	Communications Lead	Marketing and community engagement	3	t	2025-11-22 10:56:37.846115	2025-11-22 10:56:37.846115
4	Finance Manager	Financial planning and reporting	4	t	2025-11-22 10:56:37.846115	2025-11-22 10:56:37.846115
5	cordinator 	OVERSEES ALL OUTREACHES 	5	t	2025-11-29 16:16:54.795415	2025-11-29 16:16:54.795415
\.


--
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.admins_id_seq', 4, true);


--
-- Name: applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.applications_id_seq', 7, true);


--
-- Name: contact_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.contact_info_id_seq', 4, true);


--
-- Name: core_values_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.core_values_id_seq', 4, true);


--
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.countries_id_seq', 8, true);


--
-- Name: donations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.donations_id_seq', 10, true);


--
-- Name: founder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.founder_id_seq', 2, true);


--
-- Name: members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.members_id_seq', 1, false);


--
-- Name: page_content_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.page_content_id_seq', 3, true);


--
-- Name: project_images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.project_images_id_seq', 32, true);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.projects_id_seq', 10, true);


--
-- Name: regional_offices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.regional_offices_id_seq', 19, true);


--
-- Name: site_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.site_settings_id_seq', 9, true);


--
-- Name: social_media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.social_media_id_seq', 5, true);


--
-- Name: team_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.team_members_id_seq', 43, true);


--
-- Name: team_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.team_roles_id_seq', 5, true);


--
-- Name: admins admins_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_email_key UNIQUE (email);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: admins admins_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_username_key UNIQUE (username);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: contact_info contact_info_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.contact_info
    ADD CONSTRAINT contact_info_pkey PRIMARY KEY (id);


--
-- Name: core_values core_values_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.core_values
    ADD CONSTRAINT core_values_pkey PRIMARY KEY (id);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: donations donations_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.donations
    ADD CONSTRAINT donations_pkey PRIMARY KEY (id);


--
-- Name: founder founder_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.founder
    ADD CONSTRAINT founder_pkey PRIMARY KEY (id);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- Name: page_content page_content_page_name_section_key_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.page_content
    ADD CONSTRAINT page_content_page_name_section_key_key UNIQUE (page_name, section_key);


--
-- Name: page_content page_content_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.page_content
    ADD CONSTRAINT page_content_pkey PRIMARY KEY (id);


--
-- Name: project_images project_images_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_images
    ADD CONSTRAINT project_images_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: regional_offices regional_offices_country_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.regional_offices
    ADD CONSTRAINT regional_offices_country_key UNIQUE (country);


--
-- Name: regional_offices regional_offices_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.regional_offices
    ADD CONSTRAINT regional_offices_pkey PRIMARY KEY (id);


--
-- Name: site_settings site_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.site_settings
    ADD CONSTRAINT site_settings_pkey PRIMARY KEY (id);


--
-- Name: site_settings site_settings_setting_key_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.site_settings
    ADD CONSTRAINT site_settings_setting_key_key UNIQUE (setting_key);


--
-- Name: social_media social_media_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.social_media
    ADD CONSTRAINT social_media_pkey PRIMARY KEY (id);


--
-- Name: team_members team_members_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_pkey PRIMARY KEY (id);


--
-- Name: team_roles team_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_roles
    ADD CONSTRAINT team_roles_pkey PRIMARY KEY (id);


--
-- Name: idx_applications_status; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_applications_status ON public.applications USING btree (status);


--
-- Name: idx_donations_flw_ref; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_donations_flw_ref ON public.donations USING btree (flw_ref);


--
-- Name: idx_donations_payment_status; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_donations_payment_status ON public.donations USING btree (payment_status);


--
-- Name: idx_donations_transaction_id; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_donations_transaction_id ON public.donations USING btree (transaction_id);


--
-- Name: idx_project_images_order; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_project_images_order ON public.project_images USING btree (project_id, order_position);


--
-- Name: idx_project_images_project_id; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_project_images_project_id ON public.project_images USING btree (project_id);


--
-- Name: idx_projects_country; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_projects_country ON public.projects USING btree (country);


--
-- Name: idx_projects_created_at; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_projects_created_at ON public.projects USING btree (created_at DESC);


--
-- Name: idx_projects_status; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_projects_status ON public.projects USING btree (status);


--
-- Name: idx_projects_status_country; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_projects_status_country ON public.projects USING btree (status, country);


--
-- Name: idx_team_members_active; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_team_members_active ON public.team_members USING btree (is_active);


--
-- Name: idx_team_members_order; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_team_members_order ON public.team_members USING btree (order_position);


--
-- Name: idx_team_members_role_type; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_team_members_role_type ON public.team_members USING btree (role_type);


--
-- Name: donations donations_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.donations
    ADD CONSTRAINT donations_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: project_images project_images_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_images
    ADD CONSTRAINT project_images_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- Name: project_images project_images_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.project_images
    ADD CONSTRAINT project_images_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.admins(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

\unrestrict Js8w4cWXBPzLy9rhQFiC0Tf2RVk2QE8IW6hovmWTWgEYnWUkTJ2OJrIscaAwIRL

