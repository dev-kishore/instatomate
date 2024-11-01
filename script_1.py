from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Function to log in to Instagram
def login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)
    
def logout(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(5)
    more_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[3]/span/div/a')
    more_button.click()
    time.sleep(2)
    logout_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[6]/div[1]')
    logout_button.click()
    time.sleep(5)

# Function to get list of followers
def get_followers(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(5)
    followers_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a')
    followers_button.click()
    time.sleep(5)
    followers = set()
    scroll_box = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')

    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)

    while True:
        # Scroll down to load more followers
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(3)

        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        if new_height == last_height:
            break
        last_height = new_height

    # Get the follower usernames
    followers_elements = scroll_box.find_elements(By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade" and @dir="auto"]')
    for element in followers_elements:
        followers.add(element.text)

    return followers

# Function to get the accounts you are following
def get_following(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(5)
    following_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a')
    following_button.click()
    time.sleep(5)
    following = set()
    scroll_box = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]')

    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(3)

        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        if new_height == last_height:
            break
        last_height = new_height

    # Get the following usernames
    following_elements = scroll_box.find_elements(By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade" and @dir="auto"]')
    for element in following_elements:
        following.add(element.text)

    return following

# Function to unfollow accounts not in followers
def unfollow_accounts(driver, following, followers):
    for account in following:
        if account not in followers:
            driver.get(f'https://www.instagram.com/{account}/')
            time.sleep(5)
            try:
                unfollow_button = driver.find_element(By.XPATH, '//div[@class="_ap3a _aaco _aacw _aad6 _aade" and @dir="auto" and text()="Following"]')
                if unfollow_button:
                    unfollow_button.click()
                    time.sleep(3)

                    confirm_button = driver.find_element(By.XPATH, '//span[@class="x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft" and text()="Unfollow"]')
                    confirm_button.click()
                    time.sleep(5)
            except Exception as e:
                print("Check account: ", account)



# Main function
def main():
    username = os.getenv("UN")
    password = ""
    
    driver = webdriver.Chrome()
    try:
        login(driver, username, password)
        # followers = get_followers(driver, username)
        followers = {'_arun_venkatesh', 'moni_offcl_08', 'its_good_girl268174_', '___udaya._', 'mallbro_ram', '_.vetri_selvi._', 'div1424', '_.___sandy___', 'chan_yamini', 'mrstylish_girl', '__nithyaa_6', 'the_melomaniac_rd7_', 'suij_sweet_heart', 'rigi0528', 'love_song_official_46', 'rowdygirl1599', 'pretty_gurl_9425', 'goxxip.que_en316', 'kaviya30._.01', 'its_me_hemu_28', '_janani_2_5', '_.saranya._07._', 'harish_93_', 'aanithayuvaraj', 'iam_abikani', 'ab_inaya418', 'dustyy._dxxmond', 'appleoffoneseye', 'pooja_gunasekar._', 'saturo._.gojox_x10', 'unlucky_officall', '__.haxrxshwxr__', 'divya_0906', 'janani_km_1147', 'queenofmy2040', 'karthika242023', '_.unem__', '_dr_kanna', 'ravi_raghul_02', 'smartner._', '__its_me_ur_booboo__', 'd.h.i.v.y.a261327', '_.shridharan._._', 'sasikaladevi1994', 'itzz_zarax_', 'sassy_siren_17', 'nithish_kannan_nld', 'fulfill._.queen', 'barath.__.02', 'minion___z', 'thatsingingnerd_10', 'its__me_abiii', '_.black._.pearl._', 'pra.kash_77', 'raveeeenaradhu', '__mr.akash.s__', 'the_pushkar._', 'arjuney___', '_elxz._.offz._.001', 'jcelin_n', 'sk._couple_', 'bhole_baba__b_s', 'crime__creator_', 'krithika_jeyamurugan', 'simlely_girl1363', 'naveen__ammu__', 'rowdy_papa_____', '_selenopine', '_mr.grey_hearted_', 'its_me_lovable__queen', 'ni.ve1736', 'itz_me_offcl_1402', 'x._.x.anu.x._.x', 'kavi_sweety67', '_itzzz_me_aishu_', 'ig.joker144', 'its_pragadeesh_', 'r_a_rakesh_06', 'blissy2607', 'akalya5603', 'prettieprincezz1', 'aarthi5085', 'its_me_sweet_heart_0', 'mr.candy_boy_000', 'black_devil_0902', '_queen_latha_21_', '_killer_queen_2008', 'yuvathisai_0402', 'its_lilprincess26', 'vasanth___033', '_.panji._.mittai._12', '__.jacs.__', 'rooban_anbazagan', 'priya___offcl___', 'jesus_christ_._girl_2000', '_nightmare_offl_', '_mr__vk__', '__shalini_17', 'vasu9156', 'v.jayashree__30', 'varshini_bts_lubb', '__.hzmx.__', '_its._.pavi_10', 'varshinisundaresan', 'pink_feathers_2410', 'ammu_aditi_1476', '_its_geethapriya_', 'sebastin_seby', 's_single_queen_2006_', 'cri_gefellow', 'rowdy_princess_0520', 'loved_officall_1408', 'its_me_deo_lover', 'rubitha_1612', 'msqueen4477', 'sweety__dinesh_', 'ajith__234567', 'thalapathi_2001', 'saranya_saran_2526', 'sobikasobika_m', 'basheer_rizan', 'hey.sinamika25', 'its_vicky_1409', '_series_lvr_', '_catzelle_', 'ananthu.xr', 'marvin_harshu', 'jevzz._', 'heyyaa_its_nishaa', 'randy_heartz', 'karthi_ravi99', 'ha_rish6256', '__k__a__r__t__h__i__11__', 'teja_swini_79', 'mrs_lolitta_0508', 'uno._.karthii', 'hearty._.aarthi', '__jeevizz_', '_.jayuu18', '_aravind__sk', '_its_me_safrin9786', 'its._.mee._.mathi._.007', 'cvenkadesan160', 'bts_princess_2019', 'thara__offical_', '_.laxzz_.22', 'iam_pranav_54', 'vino_vinoth_12', 'jenesh_s', 'the_._queen_._15', 'cutebabyaline', 'itz__me_sivi_', 'miz._keerthi.__', 'five._.12', 'ft._ishz_', 'blushy_girl_luv', 'angel_pushparaj_2305', 'parihar_gurl', 'uno._.kikiiii', 'ms._.meow._.x', 'aakash_ak_27', '__arun__vedha__', '_kresee_', '__.pragathi__', 'ponnrarasu', 'balaji_vijay_kumar', '_jannatul___firdouse_____.28', '03harinirajendran', 'eye_killer_girl_1811', 'lazt_luvehhh_', 'latha_latha1111', 'sree__poongothai_17', 'quail.867490', 'mr_mrs_poopriya', 'cat_.girl._01', 'self_love.2706', 'kowshi__ramesh', '_meow._.girl_30_03', 'lovely_pirai____611', 'kutty_ponnu___________________', 'dharshiniswetha2024', 'vasudevan_boopathy', 'mythiliofficial22024', 'roshinimahadevan02', 'gomathi22107', 'blue_moon_539_', 'its_me_kavya367', '_._.durga._._', 'itx_.preethi._', 'blue.moondreamer', 'duke_luver___', 'cute_thamilachii', 'thara_chosen', '1767kavi', 'senthil_kumari1512', 'itme.mythili', 'itsme_blackyprincess__', '_dharshan_13', 'kavisweety7733', '__boomi_ka', 'black_moon730', 'amee_na7570is', 'itzmearjun67', 'itz_me_karthika_sri_', 'sweetpoison823', 'nandhu._.005', 'manojkumar__mohan', 'its_varshini10', 'shai_official_02', 'nivetha.317627', '__.priyoo.__05', '__parveen_official__', 'karthika__s__karthika', 'xx_mythu_xx', '___.rajesh.___96', 'jayu_paliwal2906', 'itzz_yxgii__', 'sangeetha.s534', 'nightmare_offl', 'itz_varsha_1210', 'monixxzz21', 'rosbliss_sg', 'shobana_607', 'christi_172', 'iam_wick_4360', 'abilash._.abi', 'thishya_designer', 'ameenabbas2024', 'sainithya', 'rubynini_4', 'pinklovess58', 'na.veena1198', 'nilahasini_2730', 'nithyxx_10', 'priya_vanam_18', 'harini_official_2801', 'nithyashree1456', 'ranniesha_ranyy', 'lavshri_1526', 'poongodi__official1982', '__pooja.__006', 'angel_queen9739', 'kaviyasri_3110', 'harshini__thiyagarajan'}
        print("Followers count: ", len(followers))
        following = get_following(driver, username)
        print("Following count: ", len(following))
        unfollow_accounts(driver, following, followers)
    finally:
        logout(driver, username)
        driver.quit()

if __name__ == "__main__":
    main()
