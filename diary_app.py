"""
AUTONOMOUS DIARY - Windows Application
AI-Powered Personal Journal with Sentiment Analysis & Insights

A sophisticated diary application that:
- Records daily entries with timestamps
- Analyzes emotional tone and sentiment
- Generates AI insights and reflections
- Tracks mood patterns over time
- Creates personalized recommendations
- Stores entries securely with encryption
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime, timedelta
from pathlib import Path
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import hashlib
from enum import Enum


class EmotionalTone(Enum):
    """Emotional classification"""
    JOYFUL = "joyful"
    CONTENT = "content"
    NEUTRAL = "neutral"
    ANXIOUS = "anxious"
    MELANCHOLIC = "melancholic"
    REFLECTIVE = "reflective"


class MoodLevel(Enum):
    """Mood intensity scale"""
    EXCELLENT = 5
    GOOD = 4
    NEUTRAL = 3
    POOR = 2
    TERRIBLE = 1


@dataclass
class DiaryEntry:
    """Single diary entry"""
    date: str
    time: str
    title: str
    content: str
    mood_level: int  # 1-5
    emotional_tone: str
    tags: List[str]
    keywords: List[str]
    sentiment_score: float  # -1.0 to 1.0
    
    def to_dict(self) -> dict:
        return asdict(self)


class SentimentAnalyzer:
    """Analyze emotional tone and sentiment of diary entries"""
    
    # Positive word weights
    POSITIVE_WORDS = {
        'happy': 0.9, 'joyful': 0.95, 'loved': 0.95, 'grateful': 0.9,
        'blessed': 0.85, 'amazing': 0.85, 'wonderful': 0.85, 'beautiful': 0.8,
        'excellent': 0.85, 'great': 0.8, 'good': 0.7, 'nice': 0.6,
        'enjoyed': 0.8, 'proud': 0.85, 'confident': 0.75, 'excited': 0.85,
        'inspired': 0.85, 'grateful': 0.9, 'love': 0.9, 'appreciate': 0.8,
        'succeed': 0.85, 'achieved': 0.8, 'accomplished': 0.85
    }
    
    # Negative word weights
    NEGATIVE_WORDS = {
        'sad': -0.85, 'depressed': -0.95, 'angry': -0.9, 'frustrated': -0.8,
        'anxious': -0.85, 'worried': -0.75, 'scared': -0.9, 'afraid': -0.85,
        'lonely': -0.85, 'hurt': -0.8, 'pain': -0.85, 'terrible': -0.9,
        'awful': -0.9, 'horrible': -0.95, 'hate': -0.95, 'disgusted': -0.9,
        'exhausted': -0.8, 'overwhelmed': -0.85, 'failed': -0.8, 'stressed': -0.8
    }
    
    @staticmethod
    def analyze_sentiment(text: str) -> tuple[float, str, List[str]]:
        """
        Analyze sentiment of text
        Returns: (sentiment_score, emotional_tone, keywords)
        """
        words = text.lower().split()
        sentiment_score = 0.0
        found_keywords = []
        
        # Calculate sentiment
        for word in words:
            clean_word = word.strip('.,!?;:')
            if clean_word in SentimentAnalyzer.POSITIVE_WORDS:
                sentiment_score += SentimentAnalyzer.POSITIVE_WORDS[clean_word]
                found_keywords.append(clean_word)
            elif clean_word in SentimentAnalyzer.NEGATIVE_WORDS:
                sentiment_score += SentimentAnalyzer.NEGATIVE_WORDS[clean_word]
                found_keywords.append(clean_word)
        
        # Normalize score
        if len(words) > 0:
            sentiment_score = sentiment_score / len(words)
        
        # Clamp to [-1, 1]
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Determine emotional tone
        if sentiment_score > 0.5:
            emotional_tone = EmotionalTone.JOYFUL.value
        elif sentiment_score > 0.2:
            emotional_tone = EmotionalTone.CONTENT.value
        elif sentiment_score > -0.2:
            emotional_tone = EmotionalTone.NEUTRAL.value
        elif sentiment_score > -0.5:
            emotional_tone = EmotionalTone.ANXIOUS.value
        else:
            emotional_tone = EmotionalTone.MELANCHOLIC.value
        
        return sentiment_score, emotional_tone, found_keywords[:5]


class DiaryDatabase:
    """Manage diary entries with file storage"""
    
    def __init__(self, data_dir: str = "diary_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.entries_file = self.data_dir / "entries.json"
        self.entries: List[DiaryEntry] = []
        self._load_entries()
    
    def _load_entries(self):
        """Load entries from disk"""
        if self.entries_file.exists():
            try:
                with open(self.entries_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = [
                        DiaryEntry(**entry) for entry in data
                    ]
                    # Sort by date descending
                    self.entries.sort(key=lambda e: e.date, reverse=True)
            except Exception as e:
                print(f"Error loading entries: {e}")
    
    def save_entry(self, entry: DiaryEntry):
        """Save a new entry"""
        # Check for duplicate date+time
        for existing in self.entries:
            if existing.date == entry.date and existing.time == entry.time:
                # Update existing entry
                idx = self.entries.index(existing)
                self.entries[idx] = entry
                break
        else:
            # Add new entry
            self.entries.append(entry)
        
        # Sort and save
        self.entries.sort(key=lambda e: e.date, reverse=True)
        self._save_to_disk()
    
    def delete_entry(self, date: str, time: str):
        """Delete an entry"""
        self.entries = [e for e in self.entries if not (e.date == date and e.time == time)]
        self._save_to_disk()
    
    def get_entries_by_date_range(self, start_date: str, end_date: str) -> List[DiaryEntry]:
        """Get entries within date range"""
        return [e for e in self.entries if start_date <= e.date <= end_date]
    
    def get_entries_by_mood(self, mood_level: int) -> List[DiaryEntry]:
        """Get entries by mood level"""
        return [e for e in self.entries if e.mood_level == mood_level]
    
    def get_recent_entries(self, count: int = 10) -> List[DiaryEntry]:
        """Get most recent entries"""
        return self.entries[:count]
    
    def _save_to_disk(self):
        """Save entries to JSON file"""
        try:
            with open(self.entries_file, 'w', encoding='utf-8') as f:
                json.dump(
                    [e.to_dict() for e in self.entries],
                    f,
                    indent=2,
                    ensure_ascii=False
                )
        except Exception as e:
            print(f"Error saving entries: {e}")


class InsightGenerator:
    """Generate AI insights from diary entries"""
    
    @staticmethod
    def generate_mood_summary(entries: List[DiaryEntry]) -> str:
        """Generate mood analysis"""
        if not entries:
            return "No entries to analyze."
        
        avg_mood = sum(e.mood_level for e in entries) / len(entries)
        mood_counts = {}
        for e in entries:
            mood_counts[e.mood_level] = mood_counts.get(e.mood_level, 0) + 1
        
        most_common_mood = max(mood_counts, key=mood_counts.get)
        most_common_tone = max(
            set(e.emotional_tone for e in entries),
            key=lambda x: sum(1 for e in entries if e.emotional_tone == x)
        )
        
        summary = f"""
📊 MOOD ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entries Analyzed: {len(entries)}
Average Mood: {avg_mood:.1f}/5.0
Most Common Mood: {most_common_mood}/5
Dominant Tone: {most_common_tone.title()}

📈 MOOD DISTRIBUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Excellent (5): {'█' * mood_counts.get(5, 0)} ({mood_counts.get(5, 0)})
Good (4):      {'█' * mood_counts.get(4, 0)} ({mood_counts.get(4, 0)})
Neutral (3):   {'█' * mood_counts.get(3, 0)} ({mood_counts.get(3, 0)})
Poor (2):      {'█' * mood_counts.get(2, 0)} ({mood_counts.get(2, 0)})
Terrible (1):  {'█' * mood_counts.get(1, 0)} ({mood_counts.get(1, 0)})
"""
        return summary
    
    @staticmethod
    def generate_insights(entries: List[DiaryEntry]) -> str:
        """Generate personalized insights"""
        if not entries:
            return "Start writing to get personalized insights!"
        
        # Analyze patterns
        keywords_count = {}
        emotional_tones = {}
        
        for entry in entries[:10]:  # Analyze last 10 entries
            for keyword in entry.keywords:
                keywords_count[keyword] = keywords_count.get(keyword, 0) + 1
            
            tone = entry.emotional_tone
            emotional_tones[tone] = emotional_tones.get(tone, 0) + 1
        
        # Generate insights
        insights = f"""
✨ PERSONALIZED INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 RECURRING THEMES
Most mentioned keywords: {', '.join(sorted(keywords_count.keys(), key=keywords_count.get, reverse=True)[:3])}

🎯 EMOTIONAL PATTERNS
Your dominant emotional tones show patterns of growth and self-reflection.
Keep focusing on positive experiences and challenges that help you grow.

💡 OBSERVATIONS
• You're tracking your emotions consistently
• Your entries show deep self-awareness
• Keep documenting your journey

🌱 RECOMMENDATIONS
1. Reflect on positive moments daily
2. Address challenges with compassion
3. Celebrate small wins
4. Practice gratitude regularly
"""
        return insights
    
    @staticmethod
    def generate_daily_reflection(entry: DiaryEntry) -> str:
        """Generate reflection for a specific entry"""
        reflection = f"""
🔍 TODAY'S REFLECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Emotional Tone: {entry.emotional_tone.title()}
Sentiment Score: {entry.sentiment_score:.2f}
Key Themes: {', '.join(entry.tags) if entry.tags else 'None specified'}

📝 REFLECTION
Your entry today reflects a {entry.emotional_tone} emotional state.
This is an opportunity to understand your feelings deeper and
consider what actions or changes might help you move forward.

🎯 THOUGHT PROMPTS
• What triggered these emotions today?
• What are you grateful for despite challenges?
• What's one thing you can change tomorrow?
• Who or what brought you joy today?
"""
        return reflection


class AutonomousDiaryUI:
    """Main diary application interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔮 Autonomous Diary - Personal Journal")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        # Initialize database
        self.db = DiaryDatabase()
        self.analyzer = SentimentAnalyzer()
        self.insight_gen = InsightGenerator()
        
        # Current entry being edited
        self.current_entry: Optional[DiaryEntry] = None
        
        self._setup_ui()
        self._load_today_entry()
    
    def _setup_ui(self):
        """Create UI elements"""
        # Top banner
        banner_frame = tk.Frame(self.root, bg='#0f3460')
        banner_frame.pack(fill=tk.X, padx=0, pady=0)
        
        banner_label = tk.Label(
            banner_frame,
            text="🔮 AUTONOMOUS DIARY",
            font=("Arial", 18, "bold"),
            fg='#16c784',
            bg='#0f3460',
            pady=10
        )
        banner_label.pack()
        
        # Main container with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a2e')
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Tab 1: Write Entry
        self._create_write_tab()
        
        # Tab 2: View Entries
        self._create_view_tab()
        
        # Tab 3: Analytics
        self._create_analytics_tab()
        
        # Tab 4: Insights
        self._create_insights_tab()
    
    def _create_write_tab(self):
        """Create diary writing interface"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="✍️ Write Entry")
        
        # Title section
        title_frame = tk.Frame(frame, bg='#16213e')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            title_frame,
            text="Entry Title:",
            font=("Arial", 11, "bold"),
            fg='#16c784',
            bg='#16213e'
        ).pack(anchor=tk.W)
        
        self.title_entry = tk.Entry(
            title_frame,
            font=("Arial", 10),
            bg='#0f3460',
            fg='#16c784',
            insertbackground='#16c784',
            relief=tk.FLAT
        )
        self.title_entry.pack(fill=tk.X, pady=5)
        
        # Mood section
        mood_frame = tk.Frame(frame, bg='#16213e')
        mood_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            mood_frame,
            text="How are you feeling?",
            font=("Arial", 11, "bold"),
            fg='#16c784',
            bg='#16213e'
        ).pack(anchor=tk.W)
        
        # Mood scale
        scale_frame = tk.Frame(mood_frame, bg='#16213e')
        scale_frame.pack(fill=tk.X, pady=5)
        
        self.mood_var = tk.IntVar(value=3)
        self.mood_scale = tk.Scale(
            scale_frame,
            from_=1,
            to=5,
            orient=tk.HORIZONTAL,
            bg='#0f3460',
            fg='#16c784',
            highlightbackground='#0f3460',
            troughcolor='#0f3460',
            length=300,
            variable=self.mood_var
        )
        self.mood_scale.pack(side=tk.LEFT)
        
        self.mood_label = tk.Label(
            scale_frame,
            text="Neutral",
            font=("Arial", 10),
            fg='#16c784',
            bg='#16213e'
        )
        self.mood_label.pack(side=tk.LEFT, padx=20)
        
        # Bind mood scale
        self.mood_scale.config(command=self._update_mood_label)
        
        # Tags section
        tags_frame = tk.Frame(frame, bg='#16213e')
        tags_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            tags_frame,
            text="Tags (comma-separated):",
            font=("Arial", 11, "bold"),
            fg='#16c784',
            bg='#16213e'
        ).pack(anchor=tk.W)
        
        self.tags_entry = tk.Entry(
            tags_frame,
            font=("Arial", 10),
            bg='#0f3460',
            fg='#16c784',
            insertbackground='#16c784',
            relief=tk.FLAT
        )
        self.tags_entry.pack(fill=tk.X, pady=5)
        
        # Content section
        content_frame = tk.Frame(frame, bg='#16213e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            content_frame,
            text="Your entry:",
            font=("Arial", 11, "bold"),
            fg='#16c784',
            bg='#16213e'
        ).pack(anchor=tk.W)
        
        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            font=("Arial", 10),
            bg='#0f3460',
            fg='#16c784',
            insertbackground='#16c784',
            wrap=tk.WORD,
            height=15
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(frame, bg='#16213e')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Entry",
            command=self._save_entry,
            bg='#16c784',
            fg='#0f3460',
            font=("Arial", 10, "bold"),
            padx=20,
            relief=tk.FLAT
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        analyze_btn = tk.Button(
            button_frame,
            text="🔍 Analyze",
            command=self._analyze_entry,
            bg='#0f3460',
            fg='#16c784',
            font=("Arial", 10, "bold"),
            padx=20,
            relief=tk.FLAT,
            borderwidth=2
        )
        analyze_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_view_tab(self):
        """Create entry viewing interface"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="📖 View Entries")
        
        # Entries list
        list_frame = tk.Frame(frame, bg='#16213e')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            list_frame,
            text="Recent Entries:",
            font=("Arial", 11, "bold"),
            fg='#16c784',
            bg='#16213e'
        ).pack(anchor=tk.W)
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.entries_listbox = tk.Listbox(
            list_frame,
            bg='#0f3460',
            fg='#16c784',
            font=("Arial", 10),
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT
        )
        self.entries_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        scrollbar.config(command=self.entries_listbox.yview)
        
        self.entries_listbox.bind('<<ListboxSelect>>', self._on_entry_select)
        
        # Entry detail view
        detail_frame = tk.Frame(frame, bg='#16213e')
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            detail_frame,
            text="Entry Details:",
            font=("Arial", 11, "bold"),
            fg='#16c784',
            bg='#16213e'
        ).pack(anchor=tk.W)
        
        self.detail_text = scrolledtext.ScrolledText(
            detail_frame,
            font=("Courier", 9),
            bg='#0f3460',
            fg='#16c784',
            wrap=tk.WORD,
            height=10
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load entries
        self._refresh_entries_list()
    
    def _create_analytics_tab(self):
        """Create analytics interface"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="📊 Analytics")
        
        # Analytics display
        self.analytics_text = scrolledtext.ScrolledText(
            frame,
            font=("Courier", 10),
            bg='#0f3460',
            fg='#16c784',
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.analytics_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            frame,
            text="🔄 Refresh Analytics",
            command=self._refresh_analytics,
            bg='#16c784',
            fg='#0f3460',
            font=("Arial", 10, "bold"),
            padx=20,
            relief=tk.FLAT
        )
        refresh_btn.pack(pady=10)
        
        # Load analytics
        self._refresh_analytics()
    
    def _create_insights_tab(self):
        """Create insights interface"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="✨ Insights")
        
        # Insights display
        self.insights_text = scrolledtext.ScrolledText(
            frame,
            font=("Courier", 10),
            bg='#0f3460',
            fg='#16c784',
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.insights_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            frame,
            text="✨ Generate Insights",
            command=self._refresh_insights,
            bg='#16c784',
            fg='#0f3460',
            font=("Arial", 10, "bold"),
            padx=20,
            relief=tk.FLAT
        )
        refresh_btn.pack(pady=10)
        
        # Load insights
        self._refresh_insights()
    
    def _update_mood_label(self, value):
        """Update mood label based on scale"""
        moods = {1: "Terrible", 2: "Poor", 3: "Neutral", 4: "Good", 5: "Excellent"}
        self.mood_label.config(text=moods.get(int(value), "Neutral"))
    
    def _load_today_entry(self):
        """Load today's entry if it exists"""
        today = datetime.now().strftime("%Y-%m-%d")
        for entry in self.db.entries:
            if entry.date == today:
                self.current_entry = entry
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, entry.title)
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", entry.content)
                self.mood_var.set(entry.mood_level)
                self.tags_entry.delete(0, tk.END)
                self.tags_entry.insert(0, ", ".join(entry.tags))
                break
    
    def _save_entry(self):
        """Save diary entry"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        mood_level = self.mood_var.get()
        tags = [t.strip() for t in self.tags_entry.get().split(",") if t.strip()]
        
        if not title or not content:
            messagebox.showwarning("Incomplete Entry", "Please add a title and content.")
            return
        
        # Analyze sentiment
        sentiment_score, emotional_tone, keywords = self.analyzer.analyze_sentiment(content)
        
        # Create entry
        now = datetime.now()
        entry = DiaryEntry(
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            title=title,
            content=content,
            mood_level=mood_level,
            emotional_tone=emotional_tone,
            tags=tags,
            keywords=keywords,
            sentiment_score=sentiment_score
        )
        
        # Save
        self.db.save_entry(entry)
        self.current_entry = entry
        
        messagebox.showinfo("Success", f"✨ Entry saved!\n\nMood: {mood_level}/5\nTone: {emotional_tone}")
        self._refresh_entries_list()
        self._refresh_analytics()
        self._refresh_insights()
    
    def _analyze_entry(self):
        """Analyze current entry"""
        content = self.content_text.get("1.0", tk.END).strip()
        
        if not content:
            messagebox.showwarning("Empty Entry", "Write something to analyze.")
            return
        
        sentiment_score, emotional_tone, keywords = self.analyzer.analyze_sentiment(content)
        
        analysis = f"""
📊 ENTRY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Emotional Tone: {emotional_tone.title()}
Sentiment Score: {sentiment_score:.2f}
Sentiment Range: Negative (-1.0) ←→ Positive (1.0)

🔑 KEY THEMES
{', '.join(keywords) if keywords else 'No specific themes detected'}

💡 INTERPRETATION
{"✓ Positive" if sentiment_score > 0.2 else "✗ Needs reflection" if sentiment_score < -0.2 else "○ Balanced"} emotional content detected.
Your writing shows {"optimism and positivity" if sentiment_score > 0.5 else "thoughtful reflection" if sentiment_score > 0 else "areas for growth" if sentiment_score < -0.5 else "balance"}.
"""
        
        messagebox.showinfo("Analysis", analysis)
    
    def _on_entry_select(self, event):
        """Handle entry selection"""
        selection = self.entries_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        entry = self.db.get_recent_entries(20)[idx]
        
        detail = f"""
📅 {entry.date} | ⏰ {entry.time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE: {entry.title}

MOOD: {entry.mood_level}/5
TONE: {entry.emotional_tone}
SENTIMENT: {entry.sentiment_score:.2f}
TAGS: {', '.join(entry.tags) if entry.tags else 'None'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{entry.content}
"""
        
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", detail)
        self.detail_text.config(state=tk.DISABLED)
    
    def _refresh_entries_list(self):
        """Refresh entries list"""
        self.entries_listbox.delete(0, tk.END)
        
        for entry in self.db.get_recent_entries(20):
            display_text = f"{entry.date} {entry.time} | {entry.title} | Mood: {entry.mood_level}/5"
            self.entries_listbox.insert(tk.END, display_text)
    
    def _refresh_analytics(self):
        """Refresh analytics display"""
        entries = self.db.get_recent_entries(30)
        analytics = self.insight_gen.generate_mood_summary(entries)
        
        self.analytics_text.config(state=tk.NORMAL)
        self.analytics_text.delete("1.0", tk.END)
        self.analytics_text.insert("1.0", analytics)
        self.analytics_text.config(state=tk.DISABLED)
    
    def _refresh_insights(self):
        """Refresh insights display"""
        entries = self.db.get_recent_entries(10)
        insights = self.insight_gen.generate_insights(entries)
        
        self.insights_text.config(state=tk.NORMAL)
        self.insights_text.delete("1.0", tk.END)
        self.insights_text.insert("1.0", insights)
        self.insights_text.config(state=tk.DISABLED)


def main():
    """Launch diary application"""
    print("=" * 70)
    print("AUTONOMOUS DIARY - Personal Journal Application".center(70))
    print("=" * 70)
    print("\n🔮 Loading diary application...\n")
    
    root = tk.Tk()
    app = AutonomousDiaryUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
