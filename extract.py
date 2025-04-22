import pdfplumber
import re

def extract_records(uploaded_file):
    records = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')

            for line in lines:
                # Skip headers
                if "Room" in line and "Invigilator" in line:
                    continue

                try:
                    # Match the date (e.g., 21st April 2025)
                    match = re.search(r'(\d{1,2}(st|nd|rd|th)?\s+\w+\s+\d{4})', line)
                    if not match:
                        continue
                    
                    date = match.group(1)
                    date_start = match.start()
                    
                    # Split line into before and after date
                    before_date = line[:date_start].strip()
                    after_date = line[date_start + len(date):].strip()

                    # Room is the first word
                    parts = before_date.split()
                    room = parts[0]
                    teacher = ' '.join(parts[1:])

                    # Duration is the rest
                    duration_match = re.findall(r'\d{1,2}:\d{2}\s?[AP]M', after_date)
                    duration = ' - '.join(duration_match) if len(duration_match) == 2 else after_date

                    records.append({
                        "teacher": teacher.strip(),
                        "room": room.strip(),
                        "date": date.strip(),
                        "duration": duration.strip()
                    })

                except Exception as e:
                    print(f"❌ Skipped line due to error: {e}")
                    continue

    return records
