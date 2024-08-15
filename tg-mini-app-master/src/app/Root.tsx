import { store } from '@/store'
import { SDKProvider, useLaunchParams } from '@telegram-apps/sdk-react'
import { TonConnectUIProvider } from '@tonconnect/ui-react'
import { useEffect, useMemo, type FC } from 'react'
import { Provider } from 'react-redux'
import { App } from './App.tsx'
import { ErrorBoundary } from './ErrorBoundary.tsx'

const ErrorBoundaryError: FC<{ error: unknown }> = ({ error }) => (
  <div>
    <p>An unhandled error occurred:</p>
    <blockquote>
      <code>
        {error instanceof Error
          ? error.message
          : typeof error === 'string'
            ? error
            : JSON.stringify(error)}
      </code>
    </blockquote>
  </div>
);

const Inner: FC = () => {
  const debug = useLaunchParams().startParam === 'debug';
  const manifestUrl = useMemo(() => {
    return new URL('tonconnect-manifest.json', window.location.href).toString();
  }, []);

  // Enable debug mode to see all the methods sent and events received.
  useEffect(() => {
    if (debug) {
      import('eruda').then((lib) => lib.default.init());
    }
  }, [debug]);

  return (
    <TonConnectUIProvider manifestUrl={manifestUrl}>
      <SDKProvider debug={debug}>
        <Provider store={store}>
          <App />
        </Provider>
      </SDKProvider>
    </TonConnectUIProvider>
  );
};

export const Root: FC = () => {
  useEffect(() => {
    return () => localStorage.setItem('api_key', '');
  }, [])
  return (
    <ErrorBoundary fallback={ErrorBoundaryError}>
      <Inner />
    </ErrorBoundary>
  );
}
