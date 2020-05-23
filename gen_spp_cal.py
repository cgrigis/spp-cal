#!/usr/bin/env python3

import datetime

import svgwrite
import holidays


def year_info(year):
    d = datetime.date(year, 1, 1)

    week_day = d.weekday()
    days_per_month = []

    month, day = 1, 1
    while True:
        d += datetime.timedelta(days=1)
        if d.month > month or d.year > year:
            days_per_month.append(day)
        if d.year > year:
            break

        month, day = d.month, d.day

    hol = holidays.CountryHoliday("CH", years=[year], prov="GE")

    return week_day, days_per_month, hol


def week_color(week_id):
    return {
        0: "#ff9900",
        1: "#00cc00",
        2: "#3399ff",
        3: "#ffff66",
    }[week_id]


def month_name(month):
    return [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ][month]


def day_name(week_day):
    return [
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche",
    ][week_day]


def holiday_fr(name_de):
    return {
        "Neujahrestag": "Nouvel An",
        "Pfingsten": "Pentecôte",
        "Karfreitag": "Vendredi Saint",
        "Ostern": "Pâques",
        "Ostermontag": "Lundi de Pâques",
        "Auffahrt": "Ascension",
        "Pfingstmontag": "Lun. de Pentecôte",
        "Nationalfeiertag": "Fête nationale",
        "Weihnachten": "Noël",
        "Wiederherstellung der Republik": "Rest. République",
    }.get(name_de, name_de)


def week_shift(week_id):
    return chr(ord("A") + week_id)


W, H = 1800, 2546
MG_L, MG_R, MG_T, MG_B = 50, 50, 80, 100
CT_H = 100
MT_H = 50
DT_W = 80

C_W, C_H = W - MG_L - MG_R, H - MG_T - MG_B
M_W, M_H = C_W / 6, (C_H - CT_H) / 2
D_W, D_H = M_W, (M_H - MT_H) / 31


def gen_calendar(year, week_id):
    dwg = svgwrite.Drawing(size=(W, H))

    main_grp = dwg.add(
        dwg.g(
            id="main",
            font_family="sans-serif",
        )
    )
    main_grp.translate((MG_R, MG_T))

    title_grp = main_grp.add(
        dwg.g(
            id="title",
            stroke="black",
        )
    )
    title_grp.add(
        dwg.text(
            f"Calendrier {year} — Semaines ABCD La Fève",
            insert=(C_W / 2, 40),
            text_anchor="middle",
            font_size=CT_H * 0.7,
        )
    )

    cal_grp = main_grp.add(dwg.g(id="calendar", stroke="black"))
    cal_grp.translate((0, CT_H))

    week_day, days_per_month, hol = year_info(year)

    # La Feve is open on December 31st, if it is normally an open day
    dec_31 = datetime.date(year, 12, 31)
    if dec_31.weekday() not in (0, 6):
        del hol[dec_31]

    work_day_seen = False
    for month in range(12):
        row, column = month // 6, month % 6

        month_grp = cal_grp.add(
            dwg.g(
                id=f"month{month + 1:02d}",
                stroke="black",
            )
        )
        month_grp.translate((column * M_W, row * M_H))

        month_title_grp = month_grp.add(
            dwg.g(
                id=f"month_title{month + 1:02d}",
                stroke="white",
            )
        )
        month_title_grp.add(
            dwg.rect(
                insert=(0, 0),
                size=(M_W, MT_H),
                fill="black",
            )
        )
        month_title_grp.add(
            dwg.text(
                month_name(month),
                insert=(D_W / 2, MT_H * 0.75),
                text_anchor="middle",
                font_size=MT_H * 0.8,
                fill="white",
            )
        )

        days_grp = month_grp.add(
            dwg.g(
                id=f"days{month + 1:02d}",
                stroke="black",
            )
        )
        days_grp.translate(0, MT_H)

        for day in range(days_per_month[month]):
            cell_texts = []

            date = datetime.date(year, month + 1, day + 1)
            holiday = hol.get(date)

            if holiday or week_day in (0, 6):
                fill_color = "lightgrey"

                if week_day == 0:  # Monday
                    week_nb = date.isocalendar()[1]
                    cell_texts.append(
                        dwg.text(
                            f"{week_nb}",
                            insert=(D_W - DT_W - 5, D_H * 0.7),
                            text_anchor="end",
                            font_size=D_H * 0.5,
                            font_weight="bolder",
                        )
                    )

                if holiday:
                    cell_texts.append(
                        dwg.text(
                            holiday_fr(holiday),
                            insert=(5, D_H * 0.7),
                            font_size=D_H * 0.5,
                        )
                    )

            else:
                fill_color = week_color(week_id)
                cell_texts.append(
                    dwg.text(
                        week_shift(week_id),
                        insert=((D_W - DT_W) / 2, D_H * 0.75),
                        text_anchor="middle",
                    )
                )
                work_day_seen = True

            day_grp = days_grp.add(
                dwg.g(
                    id=f"day{day + 1:02d}",
                    font_size=D_H * 0.7,
                )
            )
            day_grp.translate(0, day * D_H)

            day_grp.add(
                dwg.text(
                    f"{day_name(week_day)[0]}",
                    insert=(20, D_H * 0.7),
                    text_anchor="middle",
                )
            )
            day_grp.add(
                dwg.text(
                    f"{day + 1}",
                    insert=(55, D_H * 0.7),
                    text_anchor="middle",
                )
            )

            day_cell_grp = day_grp.add(
                dwg.g(
                    id=f"day_cell{day + 1:02d}",
                )
            )
            day_cell_grp.translate(DT_W, 0)

            day_cell = dwg.rect(
                insert=(0, 0),
                size=(D_W - DT_W, D_H),
                stroke_width=1,
                fill=fill_color,
            )

            day_cell_grp.add(day_cell)

            for cell_text in cell_texts:
                day_cell_grp.add(cell_text)

            week_day = (week_day + 1) % 7
            if week_day == 0 and work_day_seen:
                week_id = (week_id + 1) % 4

        month_rect = dwg.rect(
            insert=(0, 0),
            size=(M_W, M_H),
            stroke_width=5,
            fill_opacity=0.0,
        )
        month_grp.add(month_rect)

    return dwg.tostring()


if __name__ == "__main__":
    import argparse

    current_year = datetime.datetime.now().year

    parser = argparse.ArgumentParser(
        description="Generate shifts calendar.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=current_year,
        help="year for which to generate the calendar",
    )
    parser.add_argument(
        "--start-shift",
        "-s",
        type=str,
        choices=["A", "B", "C", "D"],
        default="A",
        help="shift for the first week",
    )
    parser.add_argument(
        "--filename",
        "-f",
        type=str,
        default="calendar_{year}.svg",
        help="file name for the generated calendar",
    )

    args = parser.parse_args()

    week_id = ord(args.start_shift) - ord("A")
    svg = gen_calendar(args.year, week_id)

    filename = args.filename.format(year=args.year)
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(svg)
