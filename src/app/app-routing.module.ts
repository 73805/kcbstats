import { NgModule } 			from '@angular/core';
import { RouterModule, Routes } 	from '@angular/router';

import { StateListComponent } 	from './state-list.component';
import { StateDetailComponent } 	from './state-detail.component';
import { ContestDetailComponent }   from './contest-detail.component';
import { TeamDetailComponent } 	from './team-detail.component';
import { AboutComponent } 		from './about.component';
import { Four04Component } 		from './four04.component';


const routes: Routes = [
	{ path: '', redirectTo: '/states', pathMatch: 'full' },
	{ path: 'states', 	component: StateListComponent },
	{ path: 'state/:id', 	component: StateDetailComponent },
	{ path: 'contest/:id',	component: ContestDetailComponent },
	{ path: 'team/:id', 	component: TeamDetailComponent },
	{ path: 'about', 		component: AboutComponent },
	{ path: '404', 		component: Four04Component },
	{ path: '**', 		redirectTo: '/404' }
];

@NgModule({
	imports: [ RouterModule.forRoot(routes) ],
	exports: [ RouterModule ]
})
export class AppRoutingModule {}