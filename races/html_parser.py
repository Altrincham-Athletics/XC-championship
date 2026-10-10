import sys
from pathlib import Path

from bs4 import BeautifulSoup


def parse_team_times(html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if table is None:
        return []

    rows = table.find_all("tr")
    if not rows:
        return []

    headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]

    try:
        name_idx = headers.index("Team Member")
        time_idx = headers.index("Time")
    except ValueError:
        return []

    results = []

    for row in rows[1:]:
        cells = row.find_all(["td", "th"])

        if len(cells) <= max(name_idx, time_idx):
            continue

        name = cells[name_idx].get_text(strip=True).title()
        time = cells[time_idx].get_text(strip=True)

        if name and time:
            results.append((name, time))

    return results

def write_csv(csv_file:Path, results:list[tuple[str,str]]):
    with csv_file.open('w') as f:
        for result in results:
            print(f'{result[0]},{result[1]}')
            print(f'{result[0]},{result[1]}', file=f)

def parse_html(html_table_file:Path, csv_file:Path):
    html_str = html_table_file.read_text()
    results = parse_team_times(html_str)
    write_csv(csv_file, results)

if __name__ == "__main__":
    html_table_file = Path(sys.argv[1])
    csv_file = Path(sys.argv[2])
    parse_html(html_table_file, csv_file)