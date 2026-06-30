from flask import Flask, render_template, request
import re
import math

from sympy import symbols, Eq, solve, sympify, factor
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

transformations = standard_transformations + (implicit_multiplication_application,)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


# ================= SMART MATH =================

def smart_math(query):
    query = query.lower().strip()
    query = query.replace("^", "**")

    x, y = symbols('x y')

    try:
        #  percentage
        match = re.match(r'(\d+)%\s*of\s*(\d+)', query)
        if match:
            return (float(match.group(1)) / 100) * float(match.group(2))

        # square root
        match = re.match(r'(square root of|sqrt)\s*(\d+)', query)
        if match:
            return math.sqrt(float(match.group(2)))

        # cube root
        match = re.match(r'(cube root of)\s*(\d+)', query)
        if match:
            return float(match.group(2)) ** (1/3)

        # algebra equation (2x + 3 = 7)
        if "=" in query:
            try:
                left, right = query.split("=")

                # 🔍 detect variables (x, y, a, etc.)
                variables = list(set(re.findall(r'[a-zA-Z]', query)))

                # only solve if ONE variable
                if len(variables) == 1:
                    var = symbols(variables[0])

                    left_expr = parse_expr(left, transformations=transformations)
                    right_expr = parse_expr(right, transformations=transformations)

                    equation = Eq(left_expr, right_expr)
                    solution = solve(equation, var)

                    if solution:
                        return f"{variables[0]} = {solution[0]}"
                    else:
                        return "No solution"

                else:
                    return "Multiple variables detected. Provide more equations."

            except:
                return None

        #  identities (x^3 + y^3 etc.)
        if "x" in query or "y" in query:
            expr = sympify(query)
            return factor(expr)

        #  basic math
        if re.match(r'^[0-9+\-*/().%\s]+$', query):
            return eval(query.replace("%", "/100"))

    except:
        return None

    return None

def detect_unit(query):
    match = re.match(r'(\d+)\s*(km|m|cm|mm)\s*(to)\s*(km|m|cm|mm)', query.lower())
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(4)

        conversions = {
            "km": 1000,
            "m": 1,
            "cm": 0.01,
            "mm": 0.001
        }

        meters = value * conversions[from_unit]
        return meters / conversions[to_unit]

    return None


def detect_currency(query):
    match = re.match(r'(\d+)\s*(usd|inr|eur|gbp)\s*(to)\s*(usd|inr|eur|gbp)', query.lower())
    if match:
        return {
            "amount": float(match.group(1)),
            "from": match.group(2).upper(),
            "to": match.group(4).upper()
        }
    return None


# ================= SEARCH =================

def search_duckduckgo(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://duckduckgo.com/")
    wait = WebDriverWait(driver, 10)

    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    results_data = []

    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
    )

    results = driver.find_elements(By.CSS_SELECTOR, "article")

    for r in results[:5]:
        try:
            title = r.find_element(By.TAG_NAME, "h2").text
            link = r.find_element(By.TAG_NAME, "a").get_attribute("href")

            desc = "No description available"

            results_data.append({
                "title": title,
                "link": link,
                "desc": desc
            })

        except:
            continue

    driver.quit()
    return results_data


# ================= ROUTE =================

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")

        # SMART MATH FIRST
        result = smart_math(query)
        if result is not None:
            return render_template(
                "result.html",
                query=query,
                is_calc=True,
                calc_result=result
            )
        
                # UNIT CONVERSION
        unit_result = detect_unit(query)
        if unit_result is not None:
            return render_template(
                "result.html",
                query=query,
                is_unit=True,
                unit_result=unit_result
            )

        #  CURRENCY (UI only for now)
        currency = detect_currency(query)
        if currency:
            return render_template(
                "result.html",
                query=query,
                is_currency=True,
                currency=currency
            )

        #  NORMAL SEARCH
        results = search_duckduckgo(query)

        return render_template(
            "result.html",
            query=query,
            results=results,
            is_calc=False
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)