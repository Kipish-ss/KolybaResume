import { CommonModule } from '@angular/common';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { MaterialModule } from '../material-module/material.module';
import { NgModule } from '@angular/core';
import { ResumeAdaptationComponent } from './components/resume-adaptation/resume-adaptation.component';
import { ResumeRoutingModule } from './resume-routing.module';
import { SearchResultsComponent } from './components/search-results/search-results.component';
import { UploadResumeComponent } from './components/upload-resume/upload-resume.component';
import { VacancyInputPopupComponent } from './components/vacancy-input-popup/vacancy-input-popup.component';

@NgModule({
    declarations: [
        UploadResumeComponent,
        ResumeAdaptationComponent,
        SearchResultsComponent,
        DashboardComponent,
        VacancyInputPopupComponent,
    ],
    imports: [
        CommonModule,
        ResumeRoutingModule,
        MaterialModule,
    ]
})
export class ResumeModule {}
