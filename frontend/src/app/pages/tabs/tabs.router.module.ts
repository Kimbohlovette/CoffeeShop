import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      { path: 'drink-menu',  loadChildren: () => import('../drink-menu/drink-menu.module').then(mod => mod.DrinkMenuPageModule) },
      { path: 'user-page', loadChildren: ()=> import('../user-page/user-page.module').then(mod =>mod.UserPagePageModule) },
      {
        path: '',
        redirectTo: '/tabs/drink-menu',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/drink-menu',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
