from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {
        'brand1': '',
        'weight1': '',
        'price1': '',
        'brand2': '',
        'weight2': '',
        'price2': ''
    }

    if request.method == 'POST':
        if 'compare' in request.form:
            # 获取表单数据
            form_data['brand1'] = request.form.get('brand1')
            form_data['weight1'] = request.form.get('weight1')
            form_data['price1'] = request.form.get('price1')

            form_data['brand2'] = request.form.get('brand2')
            form_data['weight2'] = request.form.get('weight2')
            form_data['price2'] = request.form.get('price2')

            # 计算单价
            if form_data['weight1'] and form_data['price1']:
                weight1 = float(form_data['weight1'])
                price1 = float(form_data['price1'])
                unit_price1 = price1 / weight1
            else:
                unit_price1 = 0

            if form_data['weight2'] and form_data['price2']:
                weight2 = float(form_data['weight2'])
                price2 = float(form_data['price2'])
                unit_price2 = price2 / weight2
            else:
                unit_price2 = 0

            # 计算价格差异百分比
            diff_percentage = calculate_price_difference_percentage(unit_price1, unit_price2)

            # 比较单价
            if unit_price1 < unit_price2:
                result = f"<strong>{form_data['brand1']}</strong> 更划算！\n单价为{unit_price1:.2f}元，比 <strong>{form_data['brand2']}</strong> 便宜{diff_percentage}%"
            elif unit_price1 > unit_price2:
                result = f"<strong>{form_data['brand2']}</strong> 更划算！\n单价为{unit_price2:.2f}元，比 <strong>{form_data['brand1']}</strong> 便宜{diff_percentage}%"
            else:
                result = "两个商品的价格相同！"

        elif 'clear' in request.form:
            # 清空表单数据
            form_data = {
                'brand1': '',
                'weight1': '',
                'price1': '',
                'brand2': '',
                'weight2': '',
                'price2': ''
            }
            result = None

    return render_template('index.html', result=result, form_data=form_data)


def calculate_price_difference_percentage(price1, price2):
    if price1 <= 0 or price2 <= 0:
        return None
    higher_price = max(price1, price2)
    lower_price = min(price1, price2)
    percentage = ((higher_price - lower_price) / higher_price) * 100
    return round(percentage, 1)


if __name__ == '__main__':
    app.run(debug=True)