from functions import *


def main():
    frazes = ['apple stock prices', "apple market info", "is it worth buying apple stock?"]

    driver = make_driver()
    total_df = pd.DataFrame({"Search_fraze": [], "title": [], 'add_date': []})

    for fraze in frazes:
        search_fraze = prepare_fraze(fraze)
        link = f"https://www.youtube.com/results?search_query={search_fraze}&sp=CAISAhAB"
        driver.get(link)
        time.sleep(3)

        try:
            # closing cookie info
            WebDriverWait(driver,5).until(ec.presence_of_element_located((By.XPATH,"/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]"))).click()
        except:
            pass

        # 100 scrolls to the bottom
        for i in range(10):
            html = driver.find_element(By.TAG_NAME, "html")
            html.send_keys(Keys.END)
            time.sleep(1)

        # get all video titles
        time.sleep(5)
        titles = [x.get_attribute('aria-label') for x in driver.find_elements(By.XPATH, ".//a[@id = 'video-title']")]
        titles = list(set(titles))

        df = pd.DataFrame({"Search_fraze": search_fraze.replace("+", " "), "title": [get_raw_title(title) for title in titles], "release_date": [get_add_date(title) for title in titles]})#, 'release_date': np.array([get_add_date(title) for title in titles])}) #"add_date": [get_add_date(title) for title in titles]
        total_df = pd.concat([total_df, df], ignore_index=True, sort=False)


    total_df.to_csv("titles.csv", encoding="utf-16")

    driver.quit()


if __name__ == "__main__":
    main()