CREATE DATABASE joy_of_painting;
USE joy_of_painting;

-- create eipsode table
CREATE TABLE episodes (
    episode_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    broadcast_date DATE NOT NULL
);

-- create subject table
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(255) UNIQUE NOT NULL
);

-- create colors table
CREATE TABLE colors (
    color_id SERIAL PRIMARY KEY,
    color_name VARCHAR(255) UNIQUE
);

-- create episode_subjects linking table
CREATE TABLE episode_subjects (
  episode_id INT,
  subject_id INT,
  PRIMARY KEY (episode_id, subject_id),
  FOREIGN KEY (episode_id) REFERENCES episodes(episode_id),
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- create episode_colors linking table
CREATE TABLE episode_colors (
  episode_id INT,
  color_id INT,
  PRIMARY KEY (episode_id, color_id),
  FOREIGN KEY (episode_id) REFERENCES episodes(episode_id),
  FOREIGN KEY (color_id) REFERENCES colors(color_id)
);