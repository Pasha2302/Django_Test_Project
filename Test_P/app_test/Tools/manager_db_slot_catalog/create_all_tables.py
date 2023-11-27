# currentMarketCap DECIMAL(65, 30),
# oneDayComparison DECIMAL(65, 30),

async def create_tables(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # SQL-запросы для создания таблиц
            create_table_query = """
            CREATE TABLE IF NOT EXISTS slot_catalog_all_slot (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_card VARCHAR(255),
                url_card VARCHAR(255),
                iframe_game_url TEXT,
                provider VARCHAR(255),
                release_date VARCHAR(50),
                wide_release_date VARCHAR(50),
                end_date VARCHAR(50),
                game_type VARCHAR(255),
                rtp VARCHAR(10),
                volatility VARCHAR(255),
                hit_frequency VARCHAR(255),
                max_win VARCHAR(255),
                min_bet VARCHAR(10),
                max_bet VARCHAR(10),
                layout VARCHAR(100),
                betways VARCHAR(255),
                features TEXT,
                theme VARCHAR(255),
                objects VARCHAR(255),
                genre VARCHAR(255),
                other_tags VARCHAR(255),
                technology VARCHAR(255),
                game_size VARCHAR(10),
                last_update VARCHAR(50),
                blog_articles VARCHAR(255),

                date_added DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
            )
            """
            await cur.execute(create_table_query)
