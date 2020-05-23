#!/usr/bin/env python

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

    hol = holidays.CountryHoliday('CH', years=[year], prov='GE')

    return week_day, days_per_month, hol

def week_color(week_id):
    return {
            0: '#ff9900',
            1: '#00cc00',
            2: '#3399ff',
            3: '#ffff66',
            }[week_id]

def calendar(year, week_id, name):
    dwg = svgwrite.Drawing(filename=name)

    months = dwg.add(dwg.g(id='months', stroke='black'))

    week_day, days_per_month, hol = year_info(year)

    for month in range(12):
        row, column = month // 6, month % 6

        month_grp = dwg.add(dwg.g(id='month{:02d}'.format(month), stroke='black'))

        month_rect = dwg.rect(
            insert=(
                column * 3 * svgwrite.cm,
                row * 10 * svgwrite.cm),
            size=(3 * svgwrite.cm, 10 * svgwrite.cm),
            stroke_width=5,
            fill='white',
            )

        month_grp.add(month_rect)

        for day in range(31):
            if day >= days_per_month[month]:
                fill_color = 'black'
            else:
                if week_day == 6:
                    week_id = (week_id + 1) % 4

                if datetime.date(year, month + 1, day + 1) in hol:
                    fill_color = 'gray'
                elif week_day in (0, 6):
                    fill_color = 'lightgray'
                else:
                    fill_color = week_color(week_id)

                week_day = (week_day + 1) % 7

            day_rect = dwg.rect(
                insert=(column * 3 * svgwrite.cm,
                    (row + day / 31) * 10 * svgwrite.cm),
                size=(3 * svgwrite.cm, (10 / 31) * svgwrite.cm),
                stroke_width=1,
                fill=fill_color,
                )

            month_grp.add(day_rect)

    dwg.save(pretty=True)

if __name__ == '__main__':
    calendar(2020, 3, "calendar.svg")
