"""Reminder calendar generators."""

from datetime import datetime, timedelta
from utils import BaseCalendarGenerator


class CountdownGenerator(BaseCalendarGenerator):
    """Generate countdown calendar for important dates."""
    
    def __init__(self):
        super().__init__('重要日期倒计时')
    
    def generate(self):
        """Generate countdown calendar."""
        important_dates = [
            ('高考 📝', '2026-06-07', '2026-06-09', '全国普通高等学校招生统一考试'),
            ('考研 📚', '2026-12-26', '2026-12-28', '全国硕士研究生招生考试'),
            ('情人节 💖', '2026-02-14', '2026-02-14', '西方情人节'),
            ('520表白日 💕', '2026-05-20', '2026-05-20', '网络情人节'),
            ('双十一购物节 🛒', '2026-11-11', '2026-11-11', '购物狂欢节'),
            ('双十二购物节 🎁', '2026-12-12', '2026-12-12', '年终购物节'),
            ('跨年夜 🎆', '2026-12-31', '2026-12-31', '告别2026迎接2027'),
            ('平安夜 🔔', '2026-12-24', '2026-12-24', '圣诞前夜'),
            ('圣诞节 🎄', '2026-12-25', '2026-12-25', '圣诞节'),
        ]
        
        for name, start, end, desc in important_dates:
            self.add_event(
                summary=name,
                start_date=start,
                end_date=end,
                description=desc
            )
        
        self.save('countdown.ics')


class WeeklyReminderGenerator(BaseCalendarGenerator):
    """Generate weekly reminder calendar."""
    
    def __init__(self):
        super().__init__('每周提醒')
    
    def generate(self):
        """Generate weekly reminder calendar."""
        reminders = [
            (0, '周一加油 💪', '新的一周开始了，为目标努力！'),
            (1, '周二继续 🔥', '保持昨天的干劲，继续前进！'),
            (2, '周三过半 ⚡', '一周过半，坚持就是胜利！'),
            (3, '周四冲刺 🚀', '即将迎来周末，加油冲刺！'),
            (4, '周五快乐 🎉', 'TGIF! 周末就在眼前！'),
            (5, '周六休息 😊', '好好休息，充电放松！'),
            (6, '周日准备 📅', '为下周做好准备！'),
        ]
        
        start_date = datetime.now()
        # Generate 12 weeks of reminders
        for week in range(12):
            for day_offset, summary, desc in reminders:
                date = start_date + timedelta(days=week*7 + day_offset)
                self.add_event(
                    summary=summary,
                    start_date=date.date(),
                    description=desc
                )
        
        self.save('weekly_reminder.ics')


class HealthRemindersGenerator(BaseCalendarGenerator):
    """Generate health reminder calendar."""
    
    def __init__(self):
        super().__init__('健康提醒')
    
    def generate(self):
        """Generate health reminders calendar."""
        health_tips = [
            ('💧 多喝水', '每天保持2000ml水分摄入'),
            ('🏃 运动锻炼', '每天至少30分钟有氧运动'),
            ('👀 保护眼睛', '远眺放松，避免长时间用眼'),
            ('🧘 放松身心', '深呼吸、冥想，释放压力'),
            ('🥗 健康饮食', '多吃蔬菜水果，均衡营养'),
            ('😴 规律作息', '保证7-8小时优质睡眠'),
            ('🦷 口腔护理', '早晚刷牙，饭后漱口'),
        ]
        
        start_date = datetime.now()
        # Generate 12 weeks of health reminders
        for week in range(12):
            for day, (summary, desc) in enumerate(health_tips):
                date = start_date + timedelta(days=week*7 + day)
                self.add_event(
                    summary=summary,
                    start_date=date.date(),
                    description=desc
                )
        
        self.save('health_reminders.ics')


class FinancialCalendarGenerator(BaseCalendarGenerator):
    """Generate financial calendar."""
    
    def __init__(self):
        super().__init__('财务日历')
    
    def generate(self):
        """Generate financial calendar."""
        # Monthly salary reminders
        for month in range(1, 13):
            try:
                date = datetime(2026, month, 10).date()
                self.add_event(
                    summary='💰 工资日',
                    start_date=date,
                    description='预计工资发放日'
                )
            except:
                pass
        
        # Quarterly tax deadlines
        tax_dates = [
            ('2026-04-15', '第一季度'),
            ('2026-07-15', '第二季度'),
            ('2026-10-15', '第三季度'),
            ('2027-01-15', '第四季度'),
        ]
        
        for date, quarter in tax_dates:
            self.add_event(
                summary=f'📊 {quarter}纳税申报截止',
                start_date=date,
                description=f'{quarter}纳税申报截止日期'
            )
        
        # Shopping festivals
        shopping_events = [
            ('2026-03-08', '👩 三八女王节', '妇女节购物促销'),
            ('2026-06-18', '🛍️ 618购物节', '年中大促'),
            ('2026-11-11', '🛒 双十一购物节', '全年最大促销'),
            ('2026-12-12', '🎁 双十二购物节', '年终大促'),
        ]
        
        for date, summary, desc in shopping_events:
            self.add_event(
                summary=summary,
                start_date=date,
                description=desc
            )
        
        self.save('financial_calendar.ics')
