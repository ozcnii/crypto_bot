import { useIntegration } from '@telegram-apps/react-router-integration';
import { postEvent } from '@telegram-apps/sdk';
import {
  bindMiniAppCSSVars,
  bindThemeParamsCSSVars,
  bindViewportCSSVars,
  initNavigator,
  useLaunchParams,
  useMiniApp,
  useThemeParams,
  useViewport,
} from '@telegram-apps/sdk-react';
import { AppRoot } from '@telegram-apps/telegram-ui';
import { useEffect, useMemo, useState, type FC } from 'react';
import { Navigate, Route, Router, Routes } from 'react-router-dom';

import { Notification } from '@/components';
import { routes } from '@/navigation/routes.tsx';
import { ErrorPage, LoaderPage } from '@/pages';
import { RootState } from '@/store';
import { getByJWTUser } from '@/store/userSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import { CSSTransition, TransitionGroup } from 'react-transition-group';

export const App: FC = () => {
  const lp = useLaunchParams();
  const miniApp = useMiniApp();
  const themeParams = useThemeParams();
  const viewport = useViewport();
  const dispatch = useDispatch<ThunkDispatch<RootState, any, any>>();
  const [rejected, setRejected] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    return bindMiniAppCSSVars(miniApp, themeParams);
  }, [miniApp, themeParams]);

  useEffect(() => {
    return bindThemeParamsCSSVars(themeParams);
  }, [themeParams]);

  useEffect(() => {
    return viewport && bindViewportCSSVars(viewport);
  }, [viewport]);

  const navigator = useMemo(() => initNavigator('app-navigation-state'), []);
  const [location, reactNavigator] = useIntegration(navigator);

  useEffect(() => {
    navigator.attach();
    return () => navigator.detach();
  }, [navigator]);

  useEffect(() => {
    postEvent('web_app_expand', {});
    postEvent('web_app_setup_swipe_behavior', {
      allow_vertical_swipe: false,
    });
    postEvent('web_app_set_header_color', {
      color: '#000000',
    });
    const api_key = new URLSearchParams(window.location.search).get('api_key');
    if (api_key) {
      localStorage.setItem('api_key', api_key);
    }
  }, []);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await dispatch(getByJWTUser());
        if (getByJWTUser.rejected.match(response)) {
          setRejected(true);
        }
      } catch (error) {
        console.error(error);
        setRejected(true);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, [dispatch]);

  if (loading) {
    return <LoaderPage />;
  }

  return (
    <AppRoot
      appearance={miniApp.isDark ? 'dark' : 'light'}
      platform={['macos', 'ios'].includes(lp.platform) ? 'ios' : 'base'}
    >
      <div className="page">
        <Router location={location} navigator={reactNavigator}>
          <TransitionGroup>
            <CSSTransition
              in={!rejected}
              key={location.key}
              timeout={400}
              classNames="fade"
              unmountOnExit
            >
              <Routes location={location}>
                {rejected ? (
                  <Route path="*" element={<ErrorPage />} />
                ) : (
                  routes.map((route) => <Route key={route.path} {...route} />)
                )}
                <Route
                  path="*"
                  element={
                    <Navigate to={rejected ? '/error' : '/'} replace={true} />
                  }
                />
              </Routes>
            </CSSTransition>
          </TransitionGroup>
        </Router>
      </div>
      <Notification />
    </AppRoot>
  );
};
