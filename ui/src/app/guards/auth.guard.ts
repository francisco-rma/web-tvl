import { ActivatedRouteSnapshot, CanActivateFn, RouterStateSnapshot } from "@angular/router";

export const AuthGuard: CanActivateFn = (
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot) => {
    return true;
}