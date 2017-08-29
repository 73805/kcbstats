import { BrowserModule }              from '@angular/platform-browser';
import { NgModule }                   from '@angular/core';
import { AppRoutingModule }           from './app-routing.module';

import { AngularFireModule }          from 'angularfire2';
import { AngularFireDatabaseModule }  from 'angularfire2/database';
import { environment }                from '../environments/environment';

import { AppComponent }               from './app.component';

import { StateListComponent }         from './state-list.component';
import { DetailService }              from './detail.service';
import { StateDetailComponent }       from './state-detail.component';
import { StateService }               from './state.service';

import { ContestDetailComponent }     from './contest-detail.component';
import { ContestDetailService }       from './contest-detail.service';

import { TeamDetailComponent }        from './team-detail.component';
import { TeamDetailService }          from './team-detail.service';

import { AboutComponent }             from './about.component';
import { Four04Component }            from './four04.component';

import { DataBarComponent }           from './data-bar.component';
import { WaffleComponent }            from './waffle.component';
import { FooterComponent }            from './footer.component';

import { FlagPosPipe }                from './flag-pos.pipe';
import { CurrencyPipe }               from '@angular/common';

@NgModule({
  imports: [
    BrowserModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFireDatabaseModule,
    AppRoutingModule
  ],
  exports: [
    CurrencyPipe
  ],
  declarations: [ 
    AppComponent,
    StateListComponent,
    StateDetailComponent,
    TeamDetailComponent,
    ContestDetailComponent,
    AboutComponent,
    Four04Component,
    WaffleComponent,
    DataBarComponent,
    FooterComponent,
    FlagPosPipe
  ],
  bootstrap: [ AppComponent ],
  providers: [  
    StateService,
    DetailService,
    TeamDetailService,
    ContestDetailService
  ]
})
export class AppModule {}