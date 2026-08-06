from ai_model import recommend_career


result = recommend_career(
    "Python SQL Pandas",
    "Data Science AI",
    "B.Tech"
)


for career in result:

    print(
        career["career"],
        "-",
        career["score"],
        "%"
    )