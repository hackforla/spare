import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import bn_translation from './translations/bn/translation.json';
import en_translation from './translations/en/translation.json';

i18n
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    lng: 'en',
    ns: ["common"],
    defaultNS: "common",
    resources: {
        en: {
            common: en_translation
        },
        bn: {
            common: bn_translation
        },
    },
    debug: true,
    react: { 
        useSuspense: false,
    },
    interpolation: {
      escapeValue: false,
    }
  });


export default i18n;