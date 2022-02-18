SELECT
    ts,
    news_item ->> 'headline' AS headline,
    news_item ->> 'description' AS description

FROM (
    SELECT
        ts,
        json_array_elements(result) as news_item
    FROM news_bing
) news