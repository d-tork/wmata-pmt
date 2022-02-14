# WMATA Usage Prep for PMT Reimbursement
Processes the raw WMATA SmarTrip usage download in order to sum up card usage on weekdays. Saves
file with year-month in the name for uploading as receipt in EOL.

## Usage
1. https://smartrip.wmata.com -> sign in
2. Choose **Metro card**
3. **Use History**
4. Select month, then **Submit**
5. Transaction type: **Use**, then **Submit**
6. **Export To Excel**
7. Save to this folder
8. Run the docker container, piping the CSV file to it:
```bash
docker run --rm -i -v $(pwd):/data wmata_pmt:latest < [filename].csv
```

## Manual steps (in Excel)
1. \[Steps 1-6 from above\]
2. Add column "day_of_week" as `=TEXT(WEEKDAY([@Time]),"ddd")`
3. Filter out weekends, sum up Changes column
4. Save as CSV with name pattern YYYY_MM-metro.csv
