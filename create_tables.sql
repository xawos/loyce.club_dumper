CREATE TABLE IF NOT EXISTS public.addresses
(
    address text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT addresses_pkey PRIMARY KEY (address)
        USING INDEX TABLESPACE btc
)

TABLESPACE btc;

ALTER TABLE IF EXISTS public.addresses
    OWNER to YOUR_USERNAME;

GRANT ALL ON TABLE public.addresses TO YOUR_USERNAME WITH GRANT OPTION;

CREATE INDEX IF NOT EXISTS addr
    ON public.addresses USING hash
    (address COLLATE pg_catalog."en_US.utf8" text_pattern_ops)
    TABLESPACE btc;

CREATE TABLE IF NOT EXISTS public.tempaddr
(
    address text COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE btc;

ALTER TABLE IF EXISTS public.tempaddr
    OWNER to YOUR_USERNAME;

REVOKE ALL ON TABLE public.tempaddr FROM PUBLIC;

GRANT SELECT ON TABLE public.tempaddr TO PUBLIC;

GRANT ALL ON TABLE public.tempaddr TO YOUR_USERNAME WITH GRANT OPTION;