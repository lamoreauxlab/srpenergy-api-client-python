daily_usage: dict[str, float] = {}

daily_usage["2022-09-01"] = 0.04
daily_usage["2022-09-01"] = round(daily_usage["2022-09-01"] + 0.04, 2)
daily_usage["2022-09-01"] = round(daily_usage["2022-09-01"] + 0.02, 2)
daily_usage["2022-09-01"] = round(daily_usage["2022-09-01"] + 0.11, 2)
daily_usage["2022-09-01"] = round(daily_usage["2022-09-01"] + 0.000014, 2)


daily_usage["2022-09-02"] = 0.14
daily_usage["2022-09-02"] = round(daily_usage["2022-09-02"] + 0.05, 2)
daily_usage["2022-09-02"] = round(daily_usage["2022-09-02"] + 0.044, 2)
daily_usage["2022-09-02"] = round(daily_usage["2022-09-02"] + 0.2141, 2)
daily_usage["2022-09-02"] = round(daily_usage["2022-09-02"] + 0.000114, 2)

reveal_type(daily_usage)
reveal_type(list(daily_usage.items()))
