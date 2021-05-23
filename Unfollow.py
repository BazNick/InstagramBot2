from selenium import webdriver
from selenium.webdriver.common.by import By
import user_Data
import time
import subprocess
import os
import pyautogui


class InstagramBot:

    def __init__(self, browser):
        self.browser = browser

        browser.get('https://www.instagram.com/')
        time.sleep(5)

        user_mail = browser.find_element_by_css_selector('input[type="text"]')
        user_password = browser.find_element_by_css_selector('input[type="password"]')

        # enter your login
        user_mail.send_keys(user_Data.user_mail)
        # enter your password
        user_password.send_keys(user_Data.user_password)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

        time.sleep(5)
        if browser.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF'):
            browser.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF').click()

        time.sleep(5)
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()

    def like_photos(self):
        target_user = self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        # instead of ... type the user your want to find
        target_user.send_keys('...')
        time.sleep(3)

        # instead of ... choose the user from the list and find him/her by link text
        self.browser.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div['
                                            '2]/div/div/a/div').click()

        time.sleep(5)

        # here I find the number of total post and convert string number into int type
        # then I divide total number of posts by 10 to scroll down to the bottom of the page
        # and to get all the posts
        number_of_posts = int(self.browser.find_element_by_class_name('g47SY').text)
        scrolling_formula = number_of_posts // 10

        all_images = None

        for i in range(0, scrolling_formula):
            all_images = self.browser.find_elements(By.CLASS_NAME, '_9AhH0')
            self.browser.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            time.sleep(2)

        all_images.pop().click()
        time.sleep(1)

        number = 0

        while number <= number_of_posts:
            get_color = self.browser.find_element_by_class_name('fr66n').find_element_by_tag_name('svg').get_attribute(
                'fill')
            if get_color == '#262626':
                self.browser.find_element_by_class_name('fr66n').find_element_by_tag_name('svg').click()
            if number == number_of_posts:
                break
            else:
                time.sleep(1)

                self.browser.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a').click()
            time.sleep(5)
            number += 1

        time.sleep(3)
        self.browser.close()

    def get_number_of_followings(self) -> 'returns number of subscriptions':
        try:
            # in my russian account partial_link_text gets word 'subscriptions'
            followings = self.browser.find_element(By.PARTIAL_LINK_TEXT, 'подписок').text
            following_array = followings.replace('подписок', '')
            number_array = following_array.replace(' ', '')
            final_number_of_followings = int(number_array)
            return final_number_of_followings
        except Exception:
            # here in my russian account partial_link_text gets word 'subscription'
            followings = self.browser.find_element(By.PARTIAL_LINK_TEXT, 'подписка').text
            following_array = followings.replace('подписка', '')
            number_array = following_array.replace(' ', '')
            final_number_of_followings = int(number_array)
            return final_number_of_followings

    def get_number_of_followers(self) -> 'returns number of subscriptions':
        try:
            # here in my russian account partial_link_text gets word 'subscribers'
            followings = self.browser.find_element(By.PARTIAL_LINK_TEXT, 'подписчиков').text
            following_array = followings.replace('подписчиков', '')
            number_array = following_array.replace(' ', '')
            final_number_of_followings = int(number_array)
            return final_number_of_followings
        except Exception:
            # here in my russian account partial_link_text gets word 'subscription'
            followings = self.browser.find_element(By.PARTIAL_LINK_TEXT, 'подписка').text
            following_array = followings.replace('подписка', '')
            number_array = following_array.replace(' ', '')
            final_number_of_followings = int(number_array)
            return final_number_of_followings

    def get_my_followers(self):
        self.browser.find_element(By.CLASS_NAME, 'gmFkV').click()
        time.sleep(4)
        number_of_followers = self.get_number_of_followers()
        followers = self.browser.find_element(By.XPATH,
                                              '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a') \
            .click()
        time.sleep(3)
        number = 1
        my_followers = []
        for i in range(number_of_followers):
            try:
                element_to_scroll = f'/html/body/div[5]/div/div/div[2]/ul/div/li[{number}]'
                number += 1
                element_to_scroll_by = self.browser.find_element_by_xpath(element_to_scroll)
                self.browser.execute_script('arguments[0].scrollIntoView();', element_to_scroll_by)
                time.sleep(0.1)
                link_text = self.browser.find_element_by_xpath(element_to_scroll).find_element_by_css_selector(
                    'a.FPmhX.notranslate._0imsa')
                my_followers.append(link_text.text)
            except Exception:
                continue
        for every_user in my_followers:
            with open('my_Subscribes.txt', 'a') as file_obj:
                file_obj.write(f'{every_user}\n')
        self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()
        time.sleep(1)

    def non_followers(self):
        self.browser.find_element(By.CLASS_NAME, 'gmFkV').click()
        time.sleep(4)
        list_of_followers = []
        # here (in brackets) you can define users who don't follow you back but you want to follow them anyway
        list_of_exception = ['...']
        try:
            # specify full path to your subscribers file
            # for example C:/Users/Unfollow/my_subscribes.txt
            path_1 = '...'
            with open(path_1, 'r') as file_obj_1:
                my_list = file_obj_1.readlines()
            for i in my_list:
                list_of_followers.append(i.replace('\n', ''))
        except FileNotFoundError:
            print('No such file exists!')

        end_of_list = self.get_number_of_followings()
        followings = self.browser.find_element(By.XPATH,
                                               '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a') \
            .click()
        time.sleep(3)
        number_of_analyzing_followings = 0
        number_of_following_list = 0
        while True:
            try:
                element_to_scroll = f'/html/body/div[5]/div/div/div[2]/ul/div/li[{number_of_following_list + 1}]'
                element_to_scroll_by = self.browser.find_element_by_xpath(element_to_scroll)
                self.browser.execute_script('arguments[0].scrollIntoView();', element_to_scroll_by)
                time.sleep(0.5)
                link_text = self.browser.find_element_by_xpath(element_to_scroll).find_element_by_css_selector(
                    'a.FPmhX.notranslate._0imsa')
                number_of_following_list += 1
                try:
                    if number_of_following_list == end_of_list:
                        break
                except Exception:
                    continue
                if link_text.text in list_of_exception:
                    continue
                else:
                    if link_text.text in list_of_followers:
                        continue
                    elif link_text.text not in list_of_followers:
                        with open('those_who_dont_follow_me_back.txt', 'a') as f_obj:
                            f_obj.write(f'{link_text.text}\n')
                        self.browser.find_element_by_xpath(element_to_scroll).find_element_by_css_selector(
                            'button.sqdOP.L3NKy._8A5w5').click()
                        time.sleep(1.5)
                        self.browser.find_element_by_css_selector('button.aOOlW.-Cab_').click()
                        time.sleep(2)
                        number_of_analyzing_followings += 1
                        print('Number of unsubscription:', number_of_analyzing_followings)
            except Exception:
                continue
            #     here you can specify how many unsubscriptions you want to make
            if number_of_analyzing_followings == 15:
                break
        self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()
        time.sleep(2)
        # this instruction tells browser to update on the page number of subscriptions
        self.browser.refresh()
        time.sleep(4)

    def copy_unfollow(self):
        time.sleep(1)
        # on mac type 'command', 'a'
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        # on mac type 'command', 'c'
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        fw = pyautogui.getActiveWindow()
        fw.close()
        time.sleep(1)
        # here you have to specify full path to your List of people I have unsubscribed from.txt file
        # for example C:/Users/Unfollow/List of people I have unsubscribed from.txt
        subprocess.Popen('...', shell=True)
        time.sleep(1)
        # on mac type 'command', 'v'
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        # on mac type 'command', 's'
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        fw = pyautogui.getActiveWindow()
        fw.close()

    def split_users_into_files(self):
        # path to your directory where files with subscribes and unsubscribes store
        # for example C:/Users/PycharmProjects/Unfollow
        path = '...'

        time.sleep(2)
        for f in os.listdir(path):
            if f == 'those_who_dont_follow_me_back.txt':
                subprocess.Popen(path + f"/{f}", shell=True)
                self.copy_unfollow()

        time.sleep(1)

        # removes file from current path for convenience
        for f in os.listdir(path):
            if f == 'those_who_dont_follow_me_back.txt':
                os.remove(path + f"/{f}")


if __name__ == '__main__':
    # in executable_path type path to your driver
    session = webdriver.Chrome(executable_path='...')
    # little report of how long it took to analyze and unfollow users
    start = time.time()
    my_bot = InstagramBot(session)
    my_bot.get_my_followers()
    my_bot.non_followers()
    session.close()

    my_bot.split_users_into_files()

    end = time.time()
    print('\n')
    print('Finish working.\n')
    print(f'Time spent: {end - start}')
