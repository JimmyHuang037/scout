import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TeacherService } from '../shared/teacher.service';
import { Teacher, StudentScore, Class, Student } from '../shared/models';
import { ProfileComponent } from './dashboard/profile/profile.component';
import { ScoresComponent } from './dashboard/scores/scores.component';
import { ClassesComponent } from './dashboard/classes/classes.component';
import { StudentsComponent } from './dashboard/students/students.component';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-teacher-dashboard',
  standalone: true,
  imports: [
    ProfileComponent, 
    ScoresComponent, 
    ClassesComponent,
    StudentsComponent,
    MatCardModule,
    MatToolbarModule
  ],
  template: `
    @if (teacherId) {
      <div class="dashboard-container">
        <mat-toolbar color="primary">
          <span>欢迎, {{teacher?.teacher_name}}!</span>
        </mat-toolbar>
        
        <div class="dashboard-content">
          <app-profile [teacher]="teacher" />
          <app-scores [scores]="scores" [loading]="scoresLoading" />
          <app-classes [classes]="classes" [loading]="classesLoading" />
          <app-students [students]="students" [loading]="studentsLoading" />
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
    .dashboard-content > * {
      margin: 16px 0;
    }
  `]
})
export class DashboardComponent implements OnInit {
  teacherId: number | null = null;
  
  teacher: Teacher | null = null;
  scores: StudentScore[] = [];
  classes: Class[] = [];
  students: Student[] = [];
  scoresLoading = false;
  classesLoading = false;
  studentsLoading = false;

  constructor(
    private teacherService: TeacherService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.teacherId = params['teacherId'] ? +params['teacherId'] : null;
      if (this.teacherId) {
        this.loadTeacherData();
      }
    });
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
}