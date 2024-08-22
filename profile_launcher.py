import os, json, re
import asyncio
import requests, time, random
from playwright.async_api import async_playwright, expect
from pathlib import Path
from fake_useragent import UserAgent
from link_mail import main as link_mail

metamask_path = "~/.config/google-chrome/Default/Extensions/nkbihfbeogaeaoehlefnkodbefgpgknn/12.0.0_0"
        
MM_PASSWORD = 'ggviva17k17'


async def main(seed,id):
     
        async with async_playwright() as p:
            user_agent = UserAgent().random
            context = await p.chromium.launch_persistent_context(
                user_data_dir='',
                headless=False,
                user_agent=user_agent,
                proxy={
                    'server': 'http://88.216.183.13:54947',#residential proxy 1 for all bottles
                    'username': 'BLDAPG07',
                    'password': 'LG62T02Q'
                },
                args=[
                    # '--headless=new',
                    '--disable-blink-features=AutomationControlled',
                    f"--disable-extensions-except={metamask_path}",
                    f"--load-extension={metamask_path}",
                ],
                color_scheme="dark",)
          
           
            print(seed)
            try:
                await launch(context=context,seed=seed,id=id)            
            except:
                 print('exception')

            # await context.close()
            

async def launch(context,seed,id):
        
        mm_page = context.pages[0]
        await mm_page.goto("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome")
        await mm_page.wait_for_load_state()

        # -------------------- согласиться с условиями использования и импортировать новый кошелек --------------------
        checkbox = mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-import-wallet')
        await create_wallet_btn.click()

        # -------------------- отказаться от сбора информации --------------------
        i_dont_agree_btn = mm_page.get_by_test_id(test_id='metametrics-no-thanks')
        await expect(i_dont_agree_btn).to_be_attached()
        await i_dont_agree_btn.click()

        # -------------------- ввести пароль --------------------
        words = seed.split(' ')
        for i in range(12):
            await mm_page.locator(f'xpath=//*[@id="import-srp__srp-word-{i}"]').fill(words[i])
            # time.sleep(0.1)
        await mm_page.locator('xpath=//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button').click()#confirm
        
        passwd_1 = mm_page.get_by_test_id(test_id='create-password-new')
        passwd_2 = mm_page.get_by_test_id(test_id='create-password-confirm')
        checkbox = mm_page.get_by_test_id(test_id='create-password-terms')
        import_wallet_btn = mm_page.locator('//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button')
        await expect(passwd_1).to_be_attached()
        await passwd_1.fill(MM_PASSWORD)
        await passwd_2.fill(MM_PASSWORD)
        await checkbox.click()
        
        await expect(import_wallet_btn).to_be_enabled()
        await import_wallet_btn.click()
        
        # -------------------- нажать "понятно" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-complete-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- нажать "далее" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-next')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- нажать "выполнено" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()
        
        # -------------------- закрыть страничку --------------------
        await asyncio.sleep(2)
        # if mm_page.locator('xpath=/html/body/div[3]/div[3]/div/section/div/button[1]'):
        #     await mm_page.locator('xpath=/html/body/div[3]/div[3]/div/section/div/button[1]').click()#enable protection
        print('mm enabled')
        await context.pages[1].close()
        #-----------------------WALLET READY TO BE USED-----------------------------
        
        # time.sleep(400)
        mm_page = context.pages[0]
        
        # await load_cookies(context)#to load worlds and join without restrictions
        print('context ready')
        # await asyncio.sleep(10)
        # await galxe_page.goto("https://app.galxe.com/quest/somnia/GC9LXtzsMS")#galxe guest page
        # await login_galxe(context)
       
        print('avatar started')
        await login_avatar(context)
        await create_avatar(context,id=id)
        print('avatar created...starting to create world')
        await create_world(context)
        await visit_5_worlds(context)

        for i in range(2):#3
            await get_a_visitor(context, id=id)
            await screenshot_3_visitors(context, world_index=id)

        await asyncio.sleep(500)
        



async def login_galxe(context):
    mm_page, galxe_page = context.pages[:2]
    try:
        login_button = galxe_page.locator("button:text('Log in')")
        await login_button.wait_for(state="visible", timeout=5000)
        await login_button.click()
        
        await galxe_page.get_by_text('Installed').first.click()#will choose MM
        print('clicked mm option')
        await asyncio.sleep(2)
        await mm_page.reload()
        await mm_page.get_by_role('button').locator('text=Next').click()
        print('clicked next')
            
            
        try:#confirm needed on 2nd and after logins still not working properly
            await asyncio.sleep(1)
            print('slept well')
            await mm_page.reload()
            await mm_page.get_by_role('button').locator('text=Confirm').click()
            print('found confirm')
        except:
            print('confirm not needed')
        await asyncio.sleep(1)
        if mm_page.get_by_role('button').locator('text=Sign-in'):
            await mm_page.get_by_role('button').locator('text=Sign-in').click()
        try:
            await asyncio.sleep(2)
            close_popup = mm_page.get_by_test_id('popover-close')
            if close_popup:
                await close_popup.click()
                print('pop-up clicked')
            else:
                print("No pop-up for MM to close")
        except:
             print('Error locating MM popup...')

            
        # cookies = await context.cookies()
        # print(cookies)
        # with open('tg.json', "w") as f:
        #     json.dump(cookies, f, indent=4)

    except:
        print('error logging in to galxe')


async def faucet_tokens(context):
    faucet_page = await context.new_page()
    await faucet_page.goto('https://faucets.chain.link/sepolia')
    



#                                           SOMNIA TASKS
async def login_avatar(context):
    avatar_page = await context.new_page()
    await avatar_page.goto('https://avatar-v2.somnia.network/')
    await avatar_page.locator('xpath=/html/body/div[6]/div/div[2]/div/div[2]/div/div/div/div/div[2]/button/span').click()#create avatar button
    await avatar_page.evaluate('document.querySelector(".mint-avatar-menu-item.mint").click()')
    await avatar_page.locator('//*[@id="__CONNECTKIT__"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/button[1]/span').click()#MM option

    mm_page = context.pages[0]
    await mm_page.reload()
    await mm_page.get_by_test_id('page-container-footer-next').click()#next
    await mm_page.get_by_test_id('page-container-footer-next').click()#confirm

    print('switching network')
    await mm_page.locator('xpath=//*[@id="app-content"]/div/div/div/div[2]/div/button[2]').click()
    print("switched")
   

async def create_avatar(context,id):
    mm_page = context.pages[0]
    page = context.pages[1]
    #select gender
    gender = random.randint(0,1)
    await asyncio.sleep(3)
    await page.locator('div.create-new-avatar-gender').nth(gender).click()
    try:
        create_avatar_btn = page.locator('body > div:nth-child(21) > div > div.ant-modal-wrap.ant-modal-centered > div > div:nth-child(2) > div > div > div > div > div.create-new-avatar-footer > button')
        await create_avatar_btn.wait_for(timeout=20000)
        print('create button found...')
        # Perform JavaScript injection to click the button
        await page.evaluate('''
            document.querySelector('body > div:nth-child(21) > div > div.ant-modal-wrap.ant-modal-centered > div > div:nth-child(2) > div > div > div > div > div.create-new-avatar-footer > button').click();
        ''')
    finally:
        print('tried..............................')
        

    
    skin_item = page.locator('body > div.inventory-container.active > div > div:nth-child(1) > div.ant-collapse-header > div')
    await skin_item.wait_for(timeout=10000)
    print('toggle found')
    #random shmotki
    for i in range(2,8):#8
        await asyncio.sleep(0.2)
        await page.evaluate(f'''
        document.querySelector('body > div.inventory-container.active > div > div:nth-child({i}) > div.ant-collapse-header > div').click();
    ''')
        print('dropdown opened')
    

    skin_item = page.locator('body > div.inventory-container.active > div > div:nth-child(1) > div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(3)')
    await skin_item.wait_for(timeout=10000)
    print('skin item found')
    for i in range(1,8):
        await asyncio.sleep(5)
        element = random.randint(1,5)
        await page.locator(f'body > div.inventory-container.active > div > div:nth-child({i}) > div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child({element})').click()
        print('random shmotka')



    #mint()
    await page.locator('xpath=/html/body/div[5]/div/div[2]/button[2]').click()#mint button
    g_name='lackre' if id==1 else 'laskan'
    await page.locator('xpath=//*[@id="name"]').fill(g_name)#fill g_name
    await page.locator("button.ant-btn.css-j9bb5n.ant-btn-primary.mint-btn").nth(1).click()
    # await page.locator('xpath=/html/body/div[9]/div/div[2]/div/div[2]/div/div/div/div[2]/form/div[2]/div/div/div/div/div/button').click()#mint button again
                            #   /html/body/div[6]/div/div[2]/div/div[2]/div/div/div/div[2]/form/div[2]/div/div/div/div/div/button
                            #   /html/body/div[9]/div/div[2]/div/div[2]/div/div/div/div[2]/form/div[2]/div/div/div/div/div/button
    await mm_page.get_by_test_id('page-container-footer-next').click()#confirm tx in MM
    print('confirmed')


async def create_world(context):
    await context.new_page()
    mm_page, page = context.pages[:2]

    await page.goto('https://playground.somnia.network/')
    await page.locator('xpath=/html/body/div[1]/div/div[9]/div[2]/button').click()#connect wallet btn                         
    await page.locator('xpath=//*[@id="__CONNECTKIT__"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[1]/div[1]/div/button[1]').click()#mm option

    await mm_page.reload()
    await mm_page.get_by_test_id('page-container-footer-next').click()#confirm tx in mm
    await mm_page.get_by_test_id('page-container-footer-next').click()#confirm tx in mm

    await page.locator('xpath=/html/body/div[1]/div/div[9]/div[2]/button').click()#create world btn
    await page.locator('xpath=//*[@id="name"]').fill('my world')
    await page.locator('xpath=/html/body/div[7]/div/div[2]/div/div[2]/div/div/div/div[2]/button').click()#create world

    await page.locator('xpath=/html/body/div[1]/div/div[9]/div[2]/button').click()#jump in
    world_url = page.url
    print(world_url)

    with open('worlds_urls.txt', 'a') as file:
        file.write(world_url + '\n')
    
    with open('3worlds.txt'):
        file.write(world_url + '\n')

    return world_url


async def visit_5_worlds(context):
    '''User should visit 5 worlds (randomly selected from file without repetitions)'''

    page = context.pages[1]

    with open('worlds_urls.txt', 'r') as file:
        worlds = file.readlines()

    worlds_to_visit = random.sample(worlds, 5)

    for w in worlds_to_visit:
        await page.goto(w)
        await asyncio.sleep(5)








#TO VISIT 3 WORLDS


async def get_a_visitor(context, id):
    page = context.pages[1]
    with open ('3worlds.txt','r') as f:
        world_url = f.readlines()[id-1]#world_url

    await page.goto(world_url)
    
    with open(f'world{id}.txt', 'a') as f:
        f.write('ready')


async def screenshot_3_visitors(context,world_index):
    page = context.pages[1]
    galxe_name = 'pisya' if world_index==1 else 'popa'

    for i in range(10):
        with open(f'worlds/world{world_index}.txt', 'r') as f:
            status = f.readlines()[0]
            if status=='readyready':#readyreadyready
                await page.screenshot(path=f"screenshots/{galxe_name}.png")

                with open(f'worlds/world{world_index}.txt', 'w') as f:
                    f.write("")
                print('screenshot done')
                return 0
            
            print('not ready to make a screenshot')
            await asyncio.sleep(3)
            













#Load cookies to join Somnia world with no errors
async def load_cookies(context):
    file_path = f"~/.config/adspower_global/cwd_global/source/cache/jikrb1d_hwf78k/sf_cookie.txt"#o1 example
    
    content = Path(file_path).expanduser()
    content = content.read_text()
    
    # Parse the JSON content
    cookies = json.loads(content)
    # Ensure that the 'secure' attribute is a boolean
    valid_cookies = []
    for cookie in cookies:
        # Convert 'secure' field to boolean if it's a string
        if isinstance(cookie.get('secure'), str):
            cookie['secure'] = cookie['secure'] == '1'

                # Convert 'http_only' field to boolean if it's a string
        if isinstance(cookie.get('http_only'), str):
            cookie['http_only'] = cookie['http_only'] == '1'

                # Convert 'same_site' field to integer if it's a string
        if isinstance(cookie.get('same_site'), str):
            cookie['same_site'] = int(cookie['same_site'])

                # Example of other potential corrections
        if 'priority' in cookie:
            try:
                cookie['priority'] = int(cookie['priority'])
            except ValueError:
                del cookie['priority']  # Remove invalid priority values

        # Validate required fields
        required_fields = ['name', 'value', 'domain', 'path']
        if all(field in cookie for field in required_fields):
            valid_cookies.append(cookie)
            
    await context.add_cookies(valid_cookies)


async def get_gid(galxe_page):
    #   GETTING MY GALXE ID (g_id)
        profile_link = await galxe_page.locator('a[href^="/id/"]').get_attribute('href')
        g_id = profile_link.rsplit('/', 1)[-1]
        print(g_id)
        return g_id


async def link_mail(context):
    '''ADD READING EMAILS FROM TABLE ACCORDING TO ACC NAME'''
    mail='ebony52_langlinaisyq@outlook.com'
    mail_password='M27Wr6EPxVApghb'
    
    galxe_page = await context.new_page()
    await galxe_page.goto('https://app.galxe.com/accountSetting/social')
    try:
        await galxe_page.get_by_placeholder('Email address').fill(mail)
        await galxe_page.get_by_role('button').get_by_text('Send a code').click()

        await asyncio.sleep(10)
        code = link_mail(mail,mail_password)
        

        await galxe_page.get_by_placeholder('Enter code').fill(code)
        await galxe_page.get_by_role('button').get_by_text('Verify').click()
    except:
        print("-----------------")
    





async def launch_async_functions():
    # seed1 = 'lava brass inherit dignity large place panel sweet saddle isolate stairs album'#o1
    seed1='party praise legal maze large wool skull cherry husband average able river'#o30
    seed2 = 'suspect latin plastic drift keen average slender acquire betray assault stove diet'#o99

    tasks = [
        asyncio.create_task(main(seed1,id=1)),
        asyncio.create_task(main(seed2, id=2)),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(launch_async_functions())


