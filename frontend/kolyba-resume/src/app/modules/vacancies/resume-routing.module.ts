import { RouterModule, Routes } from '@angular/router';

import { AuthGuard } from '@core/guards/auth.guard';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { NgModule } from '@angular/core';
import { ResumeAdaptationComponent } from './components/resume-adaptation/resume-adaptation.component';
import { SearchResultsComponent } from './components/search-results/search-results.component';
import { UploadResumeComponent } from './components/upload-resume/upload-resume.component';

const routes: Routes = [
    {
        path: '',
        component: DashboardComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'search-results',
        component: SearchResultsComponent,
        canActivate: [AuthGuard]
    },
    {
        path: '**',
        redirectTo: '',
        pathMatch: 'full',
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class ResumeRoutingModule {}