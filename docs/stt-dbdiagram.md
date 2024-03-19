# dbdiagram.io

```
Table users {
  id uuid [pk]
  first_name varchar(150)
  last_name varchar(150)
  email varchar(255) [unique]
  password varchar(255)
  is_verified boolean
}

Table ticket_holders {
  id uuid [pk]
  user_id uuid [ref: > users.id]
  first_name varchar(255)
  last_name varchar(255)
  phone varchar(255)
  address varchar(255)
  is_card_interest boolean
  is_season_ticket_interest boolean
  avatar varchar
  timezone varchar(255)
  created_at timestamp
}

Table tickets {
  id uuid [pk]
  ticket_holder_id uuid [ref: > ticket_holders.id]
  event_id uuid [ref: > events.id]
  price decimal(10, 2)
  seat varchar(255)
  row varchar(255)
  section varchar(255)
  barcode varchar(255)
  listing_status varchar(255)
  created_at timestamp
  sold_at timestamp
}

Table purchases {
  id uuid [pk]
  ticket_id uuid [ref: > tickets.id]
  invoice_number varchar(255)
  customer varchar(255)
  purchased_at timestamp
  purchase_price decimal(10, 2)
  delivery_status varchar(255)
  created_at timestamp
}

Table events {
  id uuid [pk]
  skybox_event_id varchar(255)
  name varchar(255)
  additional_info varchar(255)
  date_time timestamp
  season uuid [ref: > seasons.id]
  venue_id uuid [ref: > venues.id]
  stubhub_event_url text
  league varchar(255)
}

Table venues {
  id uuid [pk]
  skybox_venue_id int
  name varchar(255)
  address varchar(255)
  city varchar(255)
  state varchar(255)
  postal_code varchar(255)
  country varchar(255)
  timezone varchar(255)
  phone varchar(255)
}

Table teams {
  id uuid [pk]
  skybox_id int
  name varchar(255)
  description text
  name_short varchar(255)
  abbreviation varchar(255)
  league varchar(255)
  city varchar(255)
  state varchar(255)
  home_venue_id uuid [ref: > venues.id]
  logo varchar
  ticketmaster_id int
  timezone varchar(255)
  credentials_website varchar(255)
  automatiq_credentials_website_id int
  ticketmaster_name varchar(255)
  vendor_id varchar(255)
}

Table seasons {
  id uuid [pk]
  name varchar(255)
  start_year int
  league varchar(255)
  official_start_date date
  official_end_date date
  start_selling_season_date date
  start_regular_season_date date
  end_regular_season_date date
  start_playoff_date date
  end_playoff_date date
  is_selling_season boolean
  is_regular_season boolean
  is_playoff_season boolean
}

Table team_events {
  id uuid [pk]
  event_id uuid [ref: > events.id]
  team_id uuid [ref: > teams.id]
  created_at timestamp
  updated_at timestamp
}

Table ticket_holder_teams {
  id uuid [pk]
  ticket_holder_id uuid [ref: > ticket_holders.id]
  team_id uuid [ref: > teams.id]
  section varchar(255)
  row varchar(255)
  seat varchar(255)
  seats_quantity int
  credentials_website_username varchar(255)
  credentials_website_password varchar(255)
  is_confirmed boolean
  created_at timestamp
  updated_at timestamp
}
```
