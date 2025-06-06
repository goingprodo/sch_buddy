import gradio as gr
import json
import os
from datetime import datetime, timedelta
import calendar

class ScheduleManager:
    def __init__(self):
        self.base_dir = "schedule_data"
        self.week_dir = os.path.join(self.base_dir, "week")
        self.day_dir = os.path.join(self.base_dir, "day")
        self.setup_directories()
    
    def setup_directories(self):
        """필요한 디렉토리들을 생성"""
        os.makedirs(self.week_dir, exist_ok=True)
        os.makedirs(self.day_dir, exist_ok=True)
    
    def get_week_filename(self, date_str):
        """주차별 파일명 생성 (월요일 기준)"""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # 해당 주의 월요일을 찾기
        monday = date_obj - timedelta(days=date_obj.weekday())
        return f"{monday.strftime('%Y-%m-%d')}_week.json"
    
    def get_day_filename(self, date_str):
        """일별 파일명 생성"""
        return f"{date_str}.json"
    
    def load_week_data(self, date_str):
        """주간 투두리스트 로드"""
        filename = self.get_week_filename(date_str)
        filepath = os.path.join(self.week_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 기본 주간 구조 생성 (요일별 구조)
            return {
                "week_start": date_str,
                "days": {
                    "월": {"오전": [], "오후": [], "저녁": []},
                    "화": {"오전": [], "오후": [], "저녁": []},
                    "수": {"오전": [], "오후": [], "저녁": []},
                    "목": {"오전": [], "오후": [], "저녁": []},
                    "금": {"오전": [], "오후": [], "저녁": []},
                    "토": {"오전": [], "오후": [], "저녁": []},
                    "일": {"오전": [], "오후": [], "저녁": []}
                }
            }
    
    def save_week_data(self, date_str, data):
        """주간 투두리스트 저장"""
        filename = self.get_week_filename(date_str)
        filepath = os.path.join(self.week_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_day_data(self, date_str):
        """일별 체크리스트 로드"""
        # 날짜별 폴더 생성
        date_folder = os.path.join(self.day_dir, date_str)
        os.makedirs(date_folder, exist_ok=True)
        
        filename = self.get_day_filename(date_str)
        filepath = os.path.join(date_folder, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "date": date_str,
                "checklist": [],
                "completed": [],
                "notes": ""
            }
    
    def save_day_data(self, date_str, data):
        """일별 체크리스트 저장"""
        date_folder = os.path.join(self.day_dir, date_str)
        os.makedirs(date_folder, exist_ok=True)
        
        filename = self.get_day_filename(date_str)
        filepath = os.path.join(date_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_week_task(self, date_str, day, time_slot, task):
        """주간 달력에 태스크 추가"""
        data = self.load_week_data(date_str)
        if task and task not in data["days"][day][time_slot]:
            data["days"][day][time_slot].append(task)
            self.save_week_data(date_str, data)
        return data
    
    def remove_week_task(self, date_str, day, time_slot, task):
        """주간 달력에서 태스크 제거"""
        data = self.load_week_data(date_str)
        if task in data["days"][day][time_slot]:
            data["days"][day][time_slot].remove(task)
            self.save_week_data(date_str, data)
        return data
    
    def add_day_checklist(self, date_str, checklist_item):
        """일별 체크리스트 항목 추가"""
        data = self.load_day_data(date_str)
        if checklist_item and checklist_item not in data["checklist"]:
            data["checklist"].append(checklist_item)
            self.save_day_data(date_str, data)
        return self.format_day_display(data)
    
    def complete_day_checklist(self, date_str, checklist_item):
        """일별 체크리스트 항목 완료"""
        data = self.load_day_data(date_str)
        if checklist_item in data["checklist"]:
            data["checklist"].remove(checklist_item)
            if checklist_item not in data["completed"]:
                data["completed"].append(checklist_item)
                self.save_day_data(date_str, data)
        return self.format_day_display(data)
    
    def update_day_notes(self, date_str, notes):
        """일별 노트 업데이트"""
        data = self.load_day_data(date_str)
        data["notes"] = notes
        self.save_day_data(date_str, data)
        return self.format_day_display(data)
    
    def format_day_display(self, data):
        """일별 데이터 표시 형식"""
        display = f"📋 {data['date']} 체크리스트\n\n"
        display += "🔲 진행중:\n"
        for item in data["checklist"]:
            display += f"  • {item}\n"
        
        display += "\n✅ 완료됨:\n"
        for completed in data["completed"]:
            display += f"  • {completed}\n"
        
        if data["notes"]:
            display += f"\n📝 메모:\n{data['notes']}\n"
        
        return display
    
    def get_available_dates(self):
        """저장된 날짜 목록 반환"""
        week_files = []
        day_files = []
        
        if os.path.exists(self.week_dir):
            week_files = [f.replace('_week.json', '') for f in os.listdir(self.week_dir) if f.endswith('_week.json')]
        
        if os.path.exists(self.day_dir):
            for date_folder in os.listdir(self.day_dir):
                date_path = os.path.join(self.day_dir, date_folder)
                if os.path.isdir(date_path):
                    day_files.append(date_folder)
        
        return sorted(week_files), sorted(day_files)

# 스케줄 매니저 인스턴스 생성
schedule_manager = ScheduleManager()

def create_weekly_calendar_ui(date_str):
    """주간 달력 UI 생성"""
    data = schedule_manager.load_week_data(date_str)
    
    days = ["월", "화", "수", "목", "금", "토", "일"]
    time_slots = ["오전", "오후", "저녁"]
    
    # HTML 테이블로 달력 생성
    html = """
    <div style="width: 100%; margin: 20px auto;">
        <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;">
            <thead>
                <tr style="background-color: #f5f5f5;">
                    <th style="border: 1px solid #ddd; padding: 10px; text-align: center; font-weight: bold;"></th>
    """
    
    for day in days:
        html += f'<th style="border: 1px solid #ddd; padding: 10px; text-align: center; font-weight: bold; background-color: #e8f4f8;">{day}</th>'
    
    html += "</tr></thead><tbody>"
    
    for time_slot in time_slots:
        html += f'<tr><td style="border: 1px solid #ddd; padding: 10px; text-align: center; font-weight: bold; background-color: #f0f8ff;">{time_slot}</td>'
        
        for day in days:
            tasks = data["days"][day][time_slot]
            cell_content = ""
            
            if tasks:
                for task in tasks:
                    cell_content += f'<div style="background-color: #e6f3ff; margin: 2px; padding: 4px; border-radius: 3px; font-size: 12px;">📝 {task}</div>'
            
            html += f'<td style="border: 1px solid #ddd; padding: 8px; vertical-align: top; min-height: 60px;">{cell_content}</td>'
        
        html += "</tr>"
    
    html += "</tbody></table></div>"
    
    return html

def create_schedule_interface():
    """Gradio 인터페이스 생성"""
    
    # 오늘 날짜를 기본값으로 설정
    today = datetime.now().strftime("%Y-%m-%d")
    
    with gr.Blocks(title="📅 나의 일정관리", theme=gr.themes.Soft()) as interface:
        
        gr.Markdown("# 📅 나의 일정관리 시스템")
        gr.Markdown("주간 투두리스트와 일별 체크리스트를 관리하세요!")
        
        with gr.Tabs():
            # 주간 투두리스트 탭 (달력 형식)
            with gr.TabItem("📊 주간 투두리스트"):
                with gr.Row():
                    with gr.Column(scale=1):
                        week_date = gr.Textbox(
                            label="날짜 (YYYY-MM-DD)", 
                            value=today,
                            placeholder="2025-06-06"
                        )
                        
                        gr.Markdown("### 📝 일정 추가")
                        
                        day_select = gr.Dropdown(
                            label="요일 선택",
                            choices=["월", "화", "수", "목", "금", "토", "일"],
                            value="월"
                        )
                        
                        time_select = gr.Dropdown(
                            label="시간대 선택",
                            choices=["오전", "오후", "저녁"],
                            value="오전"
                        )
                        
                        task_input = gr.Textbox(
                            label="할 일 입력",
                            placeholder="예: 회의 참석, 운동하기"
                        )
                        
                        with gr.Row():
                            add_task_btn = gr.Button("➕ 추가", variant="primary")
                            load_week_btn = gr.Button("🔄 불러오기")
                        
                        gr.Markdown("### 🗑️ 일정 삭제")
                        
                        remove_day_select = gr.Dropdown(
                            label="삭제할 요일",
                            choices=["월", "화", "수", "목", "금", "토", "일"],
                            value="월"
                        )
                        
                        remove_time_select = gr.Dropdown(
                            label="삭제할 시간대",
                            choices=["오전", "오후", "저녁"],
                            value="오전"
                        )
                        
                        remove_task_select = gr.Dropdown(
                            label="삭제할 일정",
                            choices=[],
                            interactive=True
                        )
                        
                        remove_task_btn = gr.Button("🗑️ 삭제", variant="secondary")
                    
                    with gr.Column(scale=3):
                        gr.Markdown("### 📅 주간 달력")
                        weekly_calendar = gr.HTML(
                            value=create_weekly_calendar_ui(today),
                            label="주간 달력"
                        )
            
            # 일별 체크리스트 탭
            with gr.TabItem("📋 일별 체크리스트"):
                with gr.Row():
                    with gr.Column(scale=1):
                        day_date = gr.Textbox(
                            label="날짜 (YYYY-MM-DD)", 
                            value=today,
                            placeholder="2025-06-06"
                        )
                        day_checklist_input = gr.Textbox(
                            label="새 체크리스트 항목", 
                            placeholder="체크리스트 항목을 입력하세요"
                        )
                        
                        with gr.Row():
                            add_day_btn = gr.Button("➕ 추가", variant="primary")
                            load_day_btn = gr.Button("🔄 불러오기")
                        
                        day_checklist_select = gr.Dropdown(
                            label="완료할 항목 선택",
                            choices=[],
                            interactive=True
                        )
                        complete_day_btn = gr.Button("✅ 완료 처리")
                        
                        day_notes = gr.Textbox(
                            label="메모",
                            lines=4,
                            placeholder="오늘의 메모를 작성하세요"
                        )
                        save_notes_btn = gr.Button("💾 메모 저장")
                    
                    with gr.Column(scale=2):
                        day_display = gr.Textbox(
                            label="일별 체크리스트",
                            lines=15,
                            interactive=False
                        )
            
            # 데이터 조회 탭
            with gr.TabItem("📂 데이터 조회"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📅 주간 일정 조회")
                        week_search_date = gr.Textbox(
                            label="주간 조회 날짜 (YYYY-MM-DD)",
                            placeholder="2025-06-06",
                            value=""
                        )
                        view_week_btn = gr.Button("📅 주간 일정 보기")
                        
                        gr.Markdown("### 📋 일별 일정 조회")
                        day_search_date = gr.Textbox(
                            label="일별 조회 날짜 (YYYY-MM-DD)",
                            placeholder="2025-06-06", 
                            value=""
                        )
                        view_day_btn = gr.Button("📋 일별 일정 보기")
                        
                        gr.Markdown("---")
                        gr.Markdown("### 📂 저장된 데이터 목록")
                        
                        with gr.Accordion("주간 데이터 목록", open=False):
                            week_dates_list = gr.Textbox(
                                label="저장된 주간 날짜들",
                                lines=5,
                                interactive=False,
                                placeholder="저장된 데이터가 없습니다."
                            )
                            refresh_week_btn = gr.Button("🔄 주간 목록 새로고침", size="sm")
                        
                        with gr.Accordion("일별 데이터 목록", open=False):
                            day_dates_list = gr.Textbox(
                                label="저장된 일별 날짜들",
                                lines=5,
                                interactive=False,
                                placeholder="저장된 데이터가 없습니다."
                            )
                            refresh_day_btn = gr.Button("🔄 일별 목록 새로고침", size="sm")
                    
                    with gr.Column(scale=2):
                        gr.Markdown("### 📖 과거 일정 조회 (읽기 전용)")
                        
                        # 주간 일정 조회 영역
                        gr.Markdown("#### 📅 주간 달력")
                        past_weekly_calendar = gr.HTML(
                            value="<div style='text-align: center; padding: 20px; color: #666;'>📌 왼쪽에서 날짜를 입력하고 '주간 일정 보기'를 클릭하세요.</div>",
                            label="과거 주간 달력"
                        )
                        
                        # 일별 일정 조회 영역  
                        gr.Markdown("#### 📋 일별 체크리스트")
                        past_day_display = gr.Textbox(
                            label="과거 일별 체크리스트",
                            lines=10,
                            interactive=False,
                            value="📌 왼쪽에서 날짜를 입력하고 '일별 일정 보기'를 클릭하세요."
                        )
        
        # 이벤트 핸들러들
        def update_day_checklist_dropdown(date_str):
            data = schedule_manager.load_day_data(date_str)
            return gr.Dropdown(choices=data["checklist"])
        
        def update_remove_task_dropdown(date_str, day, time_slot):
            data = schedule_manager.load_week_data(date_str)
            tasks = data["days"][day][time_slot]
            return gr.Dropdown(choices=tasks)
        
        def refresh_dates_display():
            week_dates, day_dates = schedule_manager.get_available_dates()
            week_text = "\n".join(week_dates) if week_dates else "저장된 주간 데이터가 없습니다."
            day_text = "\n".join(day_dates) if day_dates else "저장된 일별 데이터가 없습니다."
            return week_text, day_text
        
        def view_past_week(date_str):
            if not date_str:
                return "<p>❌ 날짜를 선택해주세요.</p>"
            
            try:
                html = create_weekly_calendar_ui(date_str)
                # 읽기 전용임을 명시하는 스타일 추가
                readonly_html = f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 2px solid #e0e0e0;">
                    <div style="text-align: center; margin-bottom: 10px; color: #666; font-weight: bold;">
                        📖 읽기 전용 모드 - 편집 불가
                    </div>
                    {html}
                </div>
                """
                return readonly_html
            except Exception as e:
                return f"<p>❌ 데이터를 불러올 수 없습니다: {str(e)}</p>"
        
        def view_past_day(date_str):
            if not date_str:
                return "❌ 날짜를 선택해주세요."
            
            try:
                data = schedule_manager.load_day_data(date_str)
                display = f"📖 {data['date']} 체크리스트 (읽기 전용)\n\n"
                display += "🔲 할 일 목록:\n"
                for item in data["checklist"]:
                    display += f"  • {item}\n"
                
                display += "\n✅ 완료된 일:\n"
                for completed in data["completed"]:
                    display += f"  • {completed}\n"
                
                if data["notes"]:
                    display += f"\n📝 메모:\n{data['notes']}\n"
                
                if not data["checklist"] and not data["completed"] and not data["notes"]:
                    display += "\n📌 저장된 데이터가 없습니다."
                
                return display
            except Exception as e:
                return f"❌ 데이터를 불러올 수 없습니다: {str(e)}"
        
        def add_weekly_task(date_str, day, time_slot, task):
            schedule_manager.add_week_task(date_str, day, time_slot, task)
            return create_weekly_calendar_ui(date_str), ""
        
        def remove_weekly_task(date_str, day, time_slot, task):
            schedule_manager.remove_week_task(date_str, day, time_slot, task)
            return create_weekly_calendar_ui(date_str), gr.Dropdown(choices=[])
        
        def load_weekly_calendar(date_str):
            return create_weekly_calendar_ui(date_str)
        
        # 주간 달력 이벤트
        add_task_btn.click(
            add_weekly_task,
            inputs=[week_date, day_select, time_select, task_input],
            outputs=[weekly_calendar, task_input]
        )
        
        load_week_btn.click(
            load_weekly_calendar,
            inputs=[week_date],
            outputs=[weekly_calendar]
        )
        
        remove_day_select.change(
            update_remove_task_dropdown,
            inputs=[week_date, remove_day_select, remove_time_select],
            outputs=[remove_task_select]
        )
        
        remove_time_select.change(
            update_remove_task_dropdown,
            inputs=[week_date, remove_day_select, remove_time_select],
            outputs=[remove_task_select]
        )
        
        remove_task_btn.click(
            remove_weekly_task,
            inputs=[week_date, remove_day_select, remove_time_select, remove_task_select],
            outputs=[weekly_calendar, remove_task_select]
        )
        
        # 일별 체크리스트 이벤트
        add_day_btn.click(
            schedule_manager.add_day_checklist,
            inputs=[day_date, day_checklist_input],
            outputs=[day_display]
        ).then(
            lambda date: gr.update(value=""),
            inputs=[day_date],
            outputs=[day_checklist_input]
        ).then(
            update_day_checklist_dropdown,
            inputs=[day_date],
            outputs=[day_checklist_select]
        )
        
        load_day_btn.click(
            lambda date: schedule_manager.format_day_display(schedule_manager.load_day_data(date)),
            inputs=[day_date],
            outputs=[day_display]
        ).then(
            update_day_checklist_dropdown,
            inputs=[day_date],
            outputs=[day_checklist_select]
        )
        
        complete_day_btn.click(
            schedule_manager.complete_day_checklist,
            inputs=[day_date, day_checklist_select],
            outputs=[day_display]
        ).then(
            update_day_checklist_dropdown,
            inputs=[day_date],
            outputs=[day_checklist_select]
        )
        
        save_notes_btn.click(
            schedule_manager.update_day_notes,
            inputs=[day_date, day_notes],
            outputs=[day_display]
        )
        
        # 데이터 조회 이벤트
        refresh_week_btn.click(
            refresh_dates_display,
            outputs=[week_dates_list, day_dates_list]
        )
        
        refresh_day_btn.click(
            refresh_dates_display,
            outputs=[week_dates_list, day_dates_list]
        )
        
        view_week_btn.click(
            view_past_week,
            inputs=[week_search_date],
            outputs=[past_weekly_calendar]
        )
        
        view_day_btn.click(
            view_past_day,
            inputs=[day_search_date],
            outputs=[past_day_display]
        )
        
        # 초기 데이터 로드
        interface.load(
            refresh_dates_display,
            outputs=[week_dates_list, day_dates_list]
        )
    
    return interface

if __name__ == "__main__":
    # 인터페이스 생성 및 실행
    app = create_schedule_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )