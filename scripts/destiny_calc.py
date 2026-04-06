import argparse
import json
from lunar_python import Solar, Lunar
try:
    from kerykeion import AstrologicalSubject
except ImportError:
    AstrologicalSubject = None

def calculate_destiny(year, month, day, hour, minute, gender, is_lunar, lat, lng, tz_str):
    if is_lunar:
        lunar = Lunar.fromYmdHms(year, month, day, hour if hour != -1 else 12, minute, 0)
        solar = lunar.getSolar()
    else:
        solar = Solar.fromYmdHms(year, month, day, hour if hour != -1 else 12, minute, 0)
        lunar = solar.getLunar()

    ec = lunar.getEightChar()
    time_ganzhi = ec.getTime() if hour != -1 else "未知"
    
    res = {
        "eastern_bazi": {
            "solar_date": solar.toYmdHms(),
            "lunar_date": lunar.toFullString(),
            "bazi": {
                "year": ec.getYear(),
                "month": ec.getMonth(),
                "day": ec.getDay(),
                "time": time_ganzhi
            },
            "wuxing": {
                "year": ec.getYearWuXing(),
                "month": ec.getMonthWuXing(),
                "day": ec.getDayWuXing(),
                "time": ec.getTimeWuXing() if hour != -1 else "未知"
            },
            "shishen": {
                "year_gan": ec.getYearShiShenGan(), "year_zhi": ec.getYearShiShenZhi(),
                "month_gan": ec.getMonthShiShenGan(), "month_zhi": ec.getMonthShiShenZhi(),
                "day_zhi": ec.getDayShiShenZhi(),
                "time_gan": ec.getTimeShiShenGan() if hour != -1 else "未知",
                "time_zhi": ec.getTimeShiShenZhi() if hour != -1 else "未知"
            },
            "extra": {
                "minggong": ec.getMingGong(),
                "shengong": ec.getShenGong()
            }
        }
    }
    
    # Dayun
    dayun = ec.getYun(gender, 0)
    res["eastern_bazi"]["dayun_info"] = {
        "start_year": dayun.getStartYear()
    }
    
    da_yuns = dayun.getDaYun()
    dy_list = []
    for dy in da_yuns[:10]:
        dy_list.append({
            "age": dy.getStartAge(),
            "year": dy.getStartYear(),
            "ganzhi": dy.getGanZhi()
        })
    res["eastern_bazi"]["dayuns"] = dy_list

    # Western Astrology
    if AstrologicalSubject and hour != -1:
        try:
            # We use the solar date for Western astrology
            subject = AstrologicalSubject(
                "User", 
                solar.getYear(), solar.getMonth(), solar.getDay(), 
                hour, minute, 
                lat=lat, lng=lng, tz_str=tz_str, city="Custom"
            )
            
            res["western_astrology"] = {
                "sun": {
                    "sign": subject.sun.sign,
                    "house": subject.sun.house
                },
                "moon": {
                    "sign": subject.moon.sign,
                    "house": subject.moon.house
                },
                "ascendant": {
                    "sign": subject.ascendant.sign if hasattr(subject, 'ascendant') else subject.first_house.sign
                },
                "planets": {}
            }
            
            for planet in [subject.mercury, subject.venus, subject.mars, subject.jupiter, subject.saturn]:
                res["western_astrology"]["planets"][planet.name.lower()] = {
                    "sign": planet.sign,
                    "house": planet.house
                }
                
        except Exception as e:
            res["western_astrology"] = {"error": f"Astrology calculation failed: {str(e)}"}
    else:
        res["western_astrology"] = {"error": "Missing hour/minute or kerykeion not installed."}

    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", type=int, required=True)
    parser.add_argument("-m", "--month", type=int, required=True)
    parser.add_argument("-d", "--day", type=int, required=True)
    parser.add_argument("-H", "--hour", type=int, default=-1)
    parser.add_argument("-M", "--minute", type=int, default=0)
    parser.add_argument("-g", "--gender", type=int, required=True, help="1:男, 0:女")
    parser.add_argument("-l", "--lunar", action="store_true")
    parser.add_argument("--lat", type=float, default=39.9)
    parser.add_argument("--lng", type=float, default=116.4)
    parser.add_argument("--tz", type=str, default="Asia/Shanghai")
    
    args = parser.parse_args()
    try:
        result = calculate_destiny(args.year, args.month, args.day, args.hour, args.minute, args.gender, args.lunar, args.lat, args.lng, args.tz)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))