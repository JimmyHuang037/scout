import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { TeacherService } from '../shared/teacher.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Teacher, StudentScore, Class, Student } from '../shared/models';
import { ProfileComponent } from './dashboard/profile/profile.component';
import { ScoresComponent } from './dashboard/scores/scores.component';
import { ClassesComponent } from './dashboard/classes/classes.component';
import { StudentsComponent } from './dashboard/students/students.component';
import { MatTabsModule } from '@angular/material/tabs';
import { CommonModule } from '@angular/common';

interface ScoreUpdateEvent {
  teacherId: number;
  scoreId: number;
  score: number;
}

@Component({
  selector: 'app-teacher-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    ProfileComponent,
    ScoresComponent,
    ClassesComponent,
    StudentsComponent,
    MatTabsModule,
    RouterModule
  ],
  template: `
    <div class="teacher-dashboard" *ngIf="teacherId !== null">
      <h1>教师仪表板</h1>
      
      <mat-tab-group dynamicHeight>
        <mat-tab label="个人信息">
          <app-profile [teacher]="teacher"></app-profile>
        </mat-tab>
        
        <mat-tab label="成绩管理">
          <app-scores 
            [scores]="scores" 
            [loading]="scoresLoading"
            [teacherId]="teacherId"
            (scoreUpdated)="updateStudentScore($event)">
          </app-scores>
        </mat-tab>
        
        <mat-tab label="班级管理">
          <app-classes [classes]="classes" [loading]="classesLoading"></app-classes>
        </mat-tab>
        
        <mat-tab label="学生管理">
          <app-students [students]="students" [loading]="studentsLoading"></app-students>
        </mat-tab>
      </mat-tab-group>
    </div>
    
    <div *ngIf="teacherId === null" class="error-message">
      未提供教师ID参数
    </div>
  `,
  styles: [`
    .teacher-dashboard {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .error-message {
      padding: 20px;
      text-align: center;
      color: #f44336;
    }
    
    h1 {
      color: #333;
      margin-bottom: 20px;
    }
  `]
})
export class TeacherDashboardComponent implements OnInit {
  teacherId: number | null = null;
  
  teacher: Teacher | null = null;
  scores: StudentScore[] = [];
  classes: Class[] = [];
  students: Student[] = [];
  scoresLoading = false;
  classesLoading = false;
  studentsLoading = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private teacherService: TeacherService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    const teacherIdParam = this.route.snapshot.queryParamMap.get('teacherId');
    if (teacherIdParam) {
      this.teacherId = +teacherIdParam;
      this.loadTeacherData();
    } else {
      this.teacherId = null;
    }
  }

  loadTeacherData(): void {
    if (!this.teacherId) return;
    
    this.scoresLoading = true;
    this.classesLoading = true;
    this.studentsLoading = true;
    
    // 获取教师个人信息
    this.teacherService.getTeacherProfile(this.teacherId).subscribe({
      next: (teacher: Teacher) => {
        this.teacher = teacher;
        console.log("teacher:", teacher);
      },
      error: (error: any) => {
        console.error('Error loading teacher profile:', error);
      }
    });

    // 获取教师管理的学生成绩
    this.teacherService.getTeacherScores(this.teacherId).subscribe({
      next: (scores: StudentScore[]) => {
        this.scores = scores;
        this.scoresLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading teacher scores:', error);
        this.scoresLoading = false;
      }
    });

    // 获取教师管理的班级
    this.teacherService.getTeacherClasses(this.teacherId).subscribe({
      next: (classes: Class[]) => {
        this.classes = classes;
        this.classesLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading teacher classes:', error);
        this.classesLoading = false;
      }
    });

    // 获取教师管理的学生
    this.teacherService.getTeacherStudents(this.teacherId).subscribe({
      next: (students: Student[]) => {
        this.students = students;
        this.studentsLoading = false;
      },
      error: (error: any) => {
        console.error('Error loading teacher students:', error);
        this.studentsLoading = false;
      }
    });
  }

  updateStudentScore(event: ScoreUpdateEvent): void {
    this.teacherService.updateStudentScore(event.teacherId, event.scoreId, event.score)
      .subscribe({
        next: (updatedScore) => {
          // 更新本地数据
          const scoreIndex = this.scores.findIndex(s => s.score_id === event.scoreId);
          if (scoreIndex !== -1) {
            this.scores[scoreIndex] = updatedScore;
            // 使用不可变方式更新数组以触发变更检测
            this.scores = [...this.scores];
          }
          
          this.snackBar.open('成绩更新成功', '关闭', {
            duration: 3000,
          });
        },
        error: (error) => {
          console.error('更新成绩失败:', error);
          this.snackBar.open('成绩更新失败: ' + error.message, '关闭', {
            duration: 3000,
          });
        }
      });
  }
}