import css from './loader.module.css'

export const Loader = () => {
    return (
        <div className={css.container}>
            <div className={css.loader}></div>
        </div>
    );
};
