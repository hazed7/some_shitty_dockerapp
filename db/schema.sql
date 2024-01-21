-- UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Persons Table
CREATE TABLE persons (
	person_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	full_name VARCHAR(255) NOT NULL,
	phone_number VARCHAR(50) UNIQUE NOT NULL,
	date_of_birth DATE NOT NULL,
	consent_to_personal_data BOOLEAN NOT NULL DEFAULT FALSE
);

-- Document Types enum
CREATE TYPE document_type AS ENUM ('identity', 'education', 'certificates', 'cards', 'tickets', 'academic_degrees', 'military_service');

-- Documents Table
CREATE TABLE documents (
	document_id UUID NOT NULL DEFAULT uuid_generate_v4(),
	person_id UUID NOT NULL,
	document_type document_type NOT NULL,
	start_date DATE,
	end_date DATE,
	CONSTRAINT documents_pkey PRIMARY KEY (document_id, document_type),
	CONSTRAINT fk_person_document
		FOREIGN KEY(person_id)
		REFERENCES persons(person_id)
		ON DELETE CASCADE
) PARTITION BY LIST (document_type);

CREATE INDEX idx_document_person_id ON documents(person_id);

CREATE TABLE documents_identity PARTITION OF documents FOR VALUES IN ('identity');
CREATE TABLE documents_education PARTITION OF documents FOR VALUES IN ('education');
CREATE TABLE documents_certificates PARTITION OF documents FOR VALUES IN ('certificates');
CREATE TABLE documents_cards PARTITION OF documents FOR VALUES IN ('cards');
CREATE TABLE documents_tickets PARTITION OF documents FOR VALUES IN ('tickets');
CREATE TABLE documents_degrees PARTITION OF documents FOR VALUES IN ('academic_degrees');
CREATE TABLE documents_service PARTITION OF documents FOR VALUES IN ('military_service');

-- Addresses Table
CREATE TABLE addresses (
	address_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	person_id UUID NOT NULL,
	address TEXT,
	CONSTRAINT fk_person_address
		FOREIGN KEY(person_id)
		REFERENCES persons(person_id)
		ON DELETE CASCADE
);

CREATE INDEX idx_address_person_id ON addresses(person_id);

-- Work Experience Table
CREATE TABLE work_experience (
	experience_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	person_id UUID NOT NULL,
	company_name VARCHAR(255),
	job_title VARCHAR(255),
	start_date DATE,
	end_date DATE,
	rate_worked DECIMAL(10, 2) CHECK (rate_worked > 0),
	CONSTRAINT fk_person_experience
		FOREIGN KEY(person_id)
		REFERENCES persons(person_id)
		ON DELETE CASCADE
);

CREATE INDEX idx_experience_person_id ON work_experience(person_id);

-- Relatives Table
CREATE TABLE relatives (
	relative_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	person_id UUID NOT NULL,
	relative_name VARCHAR(255),
	relation_type VARCHAR(50),
	CONSTRAINT fk_person_relative
		FOREIGN KEY(person_id)
		REFERENCES persons(person_id)
		ON DELETE CASCADE
);

CREATE INDEX idx_relative_person_id ON relatives(person_id);