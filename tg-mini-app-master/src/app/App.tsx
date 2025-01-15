import { useIntegration } from '@telegram-apps/react-router-integration';
import { initViewport, postEvent, requestViewport } from '@telegram-apps/sdk';
import {
  bindMiniAppCSSVars,
  bindThemeParamsCSSVars,
  bindViewportCSSVars,
  initNavigator,
  useInitData,
  useLaunchParams,
  useMiniApp,
  useThemeParams,
  useViewport,
} from '@telegram-apps/sdk-react';
import { AppRoot } from '@telegram-apps/telegram-ui';
import { useEffect, useMemo, useRef, useState, type FC } from 'react';
import { Navigate, Route, Router, Routes } from 'react-router-dom';

import { Notification } from '@/components';
import { Stories } from '@/components/stories/stories';
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
  const [viewportHeight, setViewportHeight] = useState(0);
  const pageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const initTelegramViewport = async () => {
      const [viewport] = initViewport();
      const vp = await viewport;

      // Запрашиваем текущее состояние видимой области
      const viewportData = await requestViewport();
      setViewportHeight(viewportData.height);

      // Слушаем изменение высоты
      vp.on('change:height', (height: number) => {
        setViewportHeight(height);
      });
    };

    initTelegramViewport();
  }, []);

  // Функция управления прокруткой
  useEffect(() => {
    const manageScrolling = () => {
      const pageContent = pageRef.current;
      if (pageContent) {
        const contentHeight = pageContent.scrollHeight;

        // Если содержимое меньше или равно высоте видимой области, отключаем прокрутку
        if (contentHeight <= viewportHeight) {
          document.body.style.overflow = 'hidden';
          pageContent.style.overflow = 'hidden';
        } else {
          document.body.style.overflow = 'auto';
          pageContent.style.overflow = 'auto';
        }
      }
    };

    manageScrolling();
  }, [viewportHeight]);

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

  const initData = useInitData();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await dispatch(getByJWTUser(initData?.user?.id || 0));
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
    console.log(lp.platform);
    fetchUser();
  }, [dispatch]);

  if (loading) {
    return <LoaderPage />;
  }

  return (
    <AppRoot
      appearance={miniApp.isDark ? 'dark' : 'light'}
      platform={['macos', 'ios'].includes(lp.platform) ? 'ios' : 'base'}
      ref={pageRef}
    >
      <div className="page">
        {/* {location.pathname} */}
        <Stories />
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
                {lp.platform === 'tdesktop' ? (
                  <Route
                    path="*"
                    element={
                      <ErrorPage
                        error="Please use your phone version of telegram"
                        code={403}
                      />
                    }
                  />
                ) : rejected ? (
                  <Route
                    path="*"
                    element={
                      <ErrorPage
                        error="User not found or service is not available"
                        code={404}
                      />
                    }
                  />
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
