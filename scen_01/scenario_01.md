# Test scenario 1

## Without any implemented CM

0. Make sure that the Enermaps server is responding.
1. Get all geofiles -> should return an empty list.
2. Post NUTS/LAU geofiles -> shourd return OK.
3. Get all geofiles -> should return all NUTS/LAU geofiles that were posted at point 2.
4. Get all CMs -> should return a dict containing all CMs (empty for now).
5. Create a task for one (non existing) CM type -> should return an error.
6. Get a (non existing) task of a (non existing) cm -> should return an error.
7. Delete a (non existing) task of a (non existing) cm -> should return an error.