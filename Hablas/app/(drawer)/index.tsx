import { Stack } from 'expo-router';
import { View, Text } from 'react-native';
import { Container } from '~/components/Container';
import { ScreenContent } from '~/components/ScreenContent';

export default function Home() {
  return (
    <>
      <Stack.Screen options={{ title: 'Home' }} />
      <Container>
        <Text>Olivia what should the UI look like here?</Text>
        <ScreenContent path="app/(drawer)/index.tsx" title="Home" />
      </Container>
    </>
  );
}
