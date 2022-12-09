CREATE TABLE IF NOT EXISTS public.applehistory
(
    "Date" date NOT NULL,
    "Close" real,
    "Volume" bigint,
    "Open" real,
    "High" real,
    "Low" real,
    CONSTRAINT "appleHistory_pkey" PRIMARY KEY ("Date")
);

\copy public.applehistory FROM '$DATA_FILE' WITH (FORMAT csv, HEADER true, DELIMITER ',');
