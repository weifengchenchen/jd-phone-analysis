from DrissionPage import Chromium
from DrissionPage import ChromiumPage
# 启动或接管浏览器，并获取标签页对象
tab = ChromiumPage()
# 跳转到登录页面
tab.get('https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fitem.jd.com%2F100157830512.html&czLogin=1')

# 定位到账号文本框，获取文本框元素
ele = tab.ele('#loginname')
# 输入对文本框输入账号 #第一次登录需输入账号密码,第二次就不需要
ele.input('微风沉沉')
# 定位到密码文本框并输入密码
tab.ele('#nloginpwd').input('Qq1607561277')
# 点击登录按钮
tab.ele('#loginsubmit').click()

