
-- 1) VERIFY initial data
SELECT * FROM users   WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SELECT * FROM amenities;

-- 2) INSERT a test place and a test review
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
  'test-place-uuid-0000-0000-000000000000',
  'Test Place', 'Just a test', 10.0, 0.0, 0.0,
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
  'test-review-uuid-0000-0000-000000000000',
  'Nice!', 5,
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'test-place-uuid-0000-0000-000000000000'
);

-- 3) VERIFY inserts
SELECT * FROM places  WHERE id = 'test-place-uuid-0000-0000-000000000000';
SELECT * FROM reviews WHERE id = 'test-review-uuid-0000-0000-000000000000';

-- 4) CLEAN UP test data
DELETE FROM reviews WHERE id = 'test-review-uuid-0000-0000-000000000000';
DELETE FROM places  WHERE id = 'test-place-uuid-0000-0000-000000000000';
