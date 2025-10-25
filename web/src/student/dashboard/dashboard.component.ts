import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { StudentService } from '../../shared/student.service';
import { Student, Score, ExamResult } from '../../shared/models';
import { ProfileComponent } from './profile/profile.component';
import { ScoresComponent } from './scores/scores.component';
import { ExamsComponent } from './exams/exams.component';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    ProfileComponent, 
    ScoresComponent, 
    ExamsComponent,
    MatCardModule,
    MatToolbarModule
  ],
  template: `
    @if (studentId) {
      <div class="dashboard-container">
        <mat-toolbar color="primary">
          <span>欢迎, {{student?.student_name}}!</span>
        </mat-toolbar>
        
        <div class="dashboard-content">
          <app-profile [student]="student" />
          <app-exams [examResults]="examResults" [loading]="examsLoading" />
          <app-scores [scores]="scores" [loading]="scoresLoading" />
        </div>
      </div>
    }
  `,
  styles: [`
    .dashboard-container {
      padding: 16px;
      max-width: 1200px;
      margin: 0 auto;
    }
    .info-section {
      margin: 16px 0;
    }
  `]
})
export class DashboardComponent implements OnInit {
  studentId: string | null = null;
  
  student: Student | null = null;
  scores: Score[] = [];
  examResults: ExamResult[] = [];
  scoresLoading = false;
  examsLoading = false;

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
    
    this.scoresLoading = true;
    this.examsLoading = true;
    
    // 获取学生个人信息
    this.studentService.getStudentProfile(this.studentId).subscribe({
      next: (student: Student) => {
        this.student = student;
        console.log("student:", student);
      },
      error: (error: any) => {
        console.error('Error loading student profile:', error);
      }
    });

    // 获取学生成绩
    this.studentService.getStudentScores(this.studentId).subscribe({
      next: (scores: Score[]) => {
        this.scores = scores;
        this.scoresLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading student scores:', error);
        this.scoresLoading = false;
      }
    });

    // 获取考试结果
    this.studentService.getStudentExamResults(this.studentId).subscribe({
      next: (results: ExamResult[]) => {
        this.examResults = results;
        this.examsLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading exam results:', error);
        this.examsLoading = false;
      }
    });
  }
}