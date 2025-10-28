import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TeacherService } from '../shared/teacher.service';
import { Teacher, StudentScore } from '../shared/models';
import { TeacherProfileComponent } from './profile/profile.component';
import { TeacherScoresComponent } from './scores/scores.component';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-teacher-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatCardModule,
    MatSnackBarModule,
    TeacherProfileComponent,
    TeacherScoresComponent
  ],
  template: `
    <mat-toolbar color="primary">
      <span>教师仪表板</span>
    </mat-toolbar>
    
    <div class="dashboard-container">
      <app-teacher-profile [teacher]="teacher" />
      <app-teacher-scores 
        [scores]="scores" 
        [loading]="scoresLoading"
        (scoreUpdate)="onScoreUpdate($event)" />
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }
  `]
})
export class TeacherDashboardComponent implements OnInit {
  teacherId: number | null = null;
  teacher: Teacher | null = null;
  scores: StudentScore[] = [];
  scoresLoading = false;

  constructor(
    private route: ActivatedRoute,
    private teacherService: TeacherService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.teacherId = params['teacherId'] ? Number(params['teacherId']) : null;
      if (this.teacherId) {
        this.loadTeacherData();
      }
    });
  }

  loadTeacherData(): void {
    if (!this.teacherId) return;

    // 获取教师个人信息
    this.teacherService.getTeacherProfile(this.teacherId).subscribe({
      next: (teacher: Teacher) => {
        this.teacher = teacher;
      },
      error: (error: any) => {
        console.error('Error loading teacher profile:', error);
        this.snackBar.open('加载教师信息失败', '关闭', { duration: 3000 });
      }
    });

    // 获取学生成绩列表
    this.scoresLoading = true;
    this.teacherService.getTeacherScores(this.teacherId).subscribe({
      next: (scores: StudentScore[]) => {
        this.scores = scores;
        this.scoresLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading scores:', error);
        this.scoresLoading = false;
        this.snackBar.open('加载成绩列表失败', '关闭', { duration: 3000 });
      }
    });
  }

  onScoreUpdate(event: {scoreId: number, newScore: number}): void {
    if (!this.teacherId) return;
    
    this.teacherService.updateStudentScore(this.teacherId, event.scoreId, event.newScore).subscribe({
      next: (updatedScore: StudentScore) => {
        // 更新本地数据
        const index = this.scores.findIndex(s => s.score_id === event.scoreId);
        if (index !== -1) {
          this.scores[index] = updatedScore;
        }
        this.snackBar.open('成绩更新成功', '关闭', { duration: 3000 });
      },
      error: (error: any) => {
        console.error('Error updating score:', error);
        this.snackBar.open('成绩更新失败', '关闭', { duration: 3000 });
      }
    });
  }
}