import { useCallback } from "react";
import { useNavigation } from "expo-router";

export const useNavigatorRoute = () => {
  const { navigate } = useNavigation();

  const handleButtonPress = useCallback((routeName: string) => {
    // @ts-ignore
    navigate(routeName);
  }, [navigate]);

  return {
    handleButtonPress,
  };
};
