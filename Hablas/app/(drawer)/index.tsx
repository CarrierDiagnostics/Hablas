import React, { useState, useEffect } from 'react';
import { Stack } from 'expo-router';
import { View, Text, ScrollView } from 'react-native';
import { Container } from '~/components/Container';
import { ScreenContent } from '~/components/ScreenContent';
import EPub from 'react-native-epub-parser';

export default function Home() {
  const [epubContent, setEpubContent] = useState('');

  useEffect(() => {
    const loadEpub = async () => {
      try {
        // Use require to reference the EPUB in the assets folder
        const epubPath = require('../../assets/book.epub');
        const book = new EPub(epubPath);
        await book.parse();
        
        let content = '';
        for (let i = 1; i <= book.spine.length; i++) {
          const chapter = await book.getChapter(i);
          content += chapter.htmlContent;
        }
        
        setEpubContent(content);
      } catch (error) {
        console.error('Error loading EPUB:', error);
      }
    };

    loadEpub();
  }, []);

  return (
    <>
      <Stack.Screen options={{ title: 'EPUB Reader' }} />
      <Container>
        <ScrollView style={{ flex: 1 }}>
          <Text>{epubContent}</Text>
        </ScrollView>
        <ScreenContent path="app/(drawer)/index.tsx" title="EPUB Reader" />
      </Container>
    </>
  );
}
