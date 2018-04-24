"""
    Proceeds = Allotment x Final Share Price
"""
def compute_proceeds(allotment, final_share_price):
    return allotment*final_share_price

"""
    Total Purchase Price = Allotment x Initial Share Price
"""
def compute_total_purchase_price(allotment, initial_share_price):
    return allotment*initial_share_price

"""
    Capital Gain = Proceeds - Total Purchase Price + Commissions
"""
def compute_capital_gain(proceeds, allotment, initial_share_price, buy_commission, sell_commission):
    return proceeds - (allotment*initial_share_price+buy_commission+sell_commission)

"""
    Capital Gain Tax = Capital Gains x tax percentage/100
"""
def compute_capital_gain_tax(capital_gain, tax):
    if capital_gain <= 0:
        return 0.0
    return capital_gain*(tax/100.0)

"""
    Cost = Total Purchase Price + Commissions + Capital Gain Tax
"""
def compute_cost(allotment, initial_share_price, buy_commission, sell_commission, capital_gain_tax):
    return allotment*initial_share_price+buy_commission+sell_commission+capital_gain_tax

"""
    Net Profit = Proceeds - Cost
"""
def compute_net_profit(proceeds, cost):
    return proceeds - cost

"""
    Return on Investment = (Net Profit / Cost) x 100
"""
def compute_return_on_investment(net_profit, cost):
    return (net_profit/cost)*100

"""
    Break Even Price = (Total Purchase Price + Commissions) / Allotment
"""
def compute_break_even_price(allotment, initial_share_price, buy_commission, sell_commission):
    return (initial_share_price*allotment+buy_commission+sell_commission)/allotment
