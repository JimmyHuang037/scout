import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { StudentService } from '../shared/student.service';
import { Student, Score, ExamResult } from '../shared/student.model';
import { NgIf } from '@angular/common';
import { ProfileComponent } from './profile/profile.component';
import { ScoresComponent } from './scores/scores.component';
import { ExamsComponent } from './exams/exams.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [NgIf, ProfileComponent, ScoresComponent, ExamsComponent],
  template: `
    <div class="dashboard-container" *ngIf="studentId">
      <div class="welcome-section">
        <h2>欢迎, {{student?.student_name}}!</h2>
        <p>学号: {{student?.student_id}}</p>
        <p>班级: {{student?.class_name}}</p>
      </div>

      <app-profile [student]="student"></app-profile>
      <app-scores [scores]="scores" [loading]="loading"></app-scores>
      <app-exams [examResults]="examResults" [loading]="loading"></app-exams>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
    }

    .welcome-section {
      background-color: #e3f2fd;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 30px;
      text-align: center;
    }

    .welcome-section h2 {
      margin: 0 0 10px 0;
      color: #1976d2;
    }
  `]
})
export class DashboardComponent implements OnInit {
  studentId: string | null = null;
  
  student: Student | null = null;
  scores: Score[] = [];
  examResults: ExamResult[] = [];
  loading = false;

  constructor(
    private studentService: StudentService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.studentId = params['studentId'] || null;
      if (this.studentId) {
        this.loadStudentData();
      }
    });
  }

  loadStudentData(): void {
    if (!this.studentId) return;
    
    this.loading = true;
    
    // 获取学生个人信息
    this.studentService.getStudentProfile(this.studentId).subscribe({
      next: (student: Student) => {
        this.student = student;
      },
      error: (error: any) => {
        console.error('Error loading student profile:', error);
      }
    });

    // 获取学生成绩
    this.studentService.getStudentScores(this.studentId).subscribe({
      next: (scores: Score[]) => {
        this.scores = scores;
      },
      error: (error: any) => {
        console.error('Error loading student scores:', error);
      }
    });

    // 获取考试结果
    this.studentService.getStudentExamResults(this.studentId).subscribe({
      next: (results: ExamResult[]) => {
        this.examResults = results;
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading exam results:', error);
        this.loading = false;
      }
    });
  }
}