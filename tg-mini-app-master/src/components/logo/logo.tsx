import css from './logo.module.css'

export const Logo = () => {
  return (
    <div className={css.wrapper}>
      <svg width="37" height="37" viewBox="0 0 37 37" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path fillRule="evenodd" clipRule="evenodd" d="M29.4792 4.17857H2.0348V0.75H36.3984L36.3984 36.75H33.1257L33.1257 7.34924C21.4078 7.75229 14.1811 12.4851 9.8199 18.228C5.20259 24.3081 3.67117 31.6917 3.67116 36.75H0.398438C0.398439 31.094 2.0852 22.9061 7.2588 16.0934C11.7773 10.1434 18.8627 5.36798 29.4792 4.17857Z" fill="#EEEEEE" />
      </svg>
    </div>
  )
}
